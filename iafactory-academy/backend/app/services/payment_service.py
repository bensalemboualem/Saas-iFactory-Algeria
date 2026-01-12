"""
Payment service for Stripe integration and payment processing.
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import stripe

from app.models.payment import Payment, PaymentMethod, PaymentStatus
from app.models.course import Course
from app.models.user import User
from app.core.config import settings
from app.schemas.payment import PaymentCreate

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    """Payment processing service."""
    
    @staticmethod
    def create_checkout_session(
        db: Session,
        user: User,
        course: Course,
        success_url: str,
        cancel_url: str
    ) -> Dict[str, Any]:
        """
        Create Stripe checkout session for course purchase.
        
        Args:
            db: Database session
            user: User object
            course: Course object
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel
            
        Returns:
            Dict: Checkout session data with session ID and URL
            
        Raises:
            HTTPException: If course is free or Stripe error occurs
        """
        if course.price <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot create checkout for free course"
            )
        
        # Use discount price if available
        price = course.discount_price if course.discount_price else course.price
        
        try:
            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': course.title,
                            'description': course.short_description or course.title,
                            'images': [course.thumbnail_url] if course.thumbnail_url else [],
                        },
                        'unit_amount': int(price * 100),  # Convert to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                customer_email=user.email,
                metadata={
                    'user_id': str(user.id),
                    'course_id': str(course.id),
                    'course_title': course.title,
                },
            )
            
            # Create payment record in pending state
            payment = Payment(
                user_id=user.id,
                course_id=course.id,
                amount=Decimal(str(price)),
                currency='USD',
                payment_method=PaymentMethod.STRIPE,
                stripe_payment_id=checkout_session.id,
                status=PaymentStatus.PENDING,
            )
            
            db.add(payment)
            db.commit()
            db.refresh(payment)
            
            return {
                'session_id': checkout_session.id,
                'url': checkout_session.url,
                'payment_id': str(payment.id)
            }
            
        except stripe.error.StripeError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stripe error: {str(e)}"
            )
    
    @staticmethod
    def handle_webhook_event(db: Session, payload: bytes, signature: str) -> Dict[str, Any]:
        """
        Handle Stripe webhook events.
        
        Args:
            db: Database session
            payload: Raw webhook payload
            signature: Stripe signature header
            
        Returns:
            Dict: Processing result
            
        Raises:
            HTTPException: If signature verification fails
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid payload"
            )
        except stripe.error.SignatureVerificationError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid signature"
            )
        
        # Handle different event types
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            PaymentService._handle_checkout_completed(db, session)
        elif event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            PaymentService._handle_payment_succeeded(db, payment_intent)
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            PaymentService._handle_payment_failed(db, payment_intent)
        
        return {'status': 'success', 'event_type': event['type']}
    
    @staticmethod
    def _handle_checkout_completed(db: Session, session: Dict[str, Any]) -> None:
        """Handle successful checkout session completion."""
        metadata = session.get('metadata', {})
        user_id = metadata.get('user_id')
        course_id = metadata.get('course_id')
        
        if not user_id or not course_id:
            return
        
        # Update payment record
        payment = db.query(Payment).filter(
            Payment.stripe_payment_id == session['id']
        ).first()
        
        if payment:
            payment.status = PaymentStatus.COMPLETED
            payment.paid_at = datetime.utcnow()
            db.commit()
            
            # Auto-enroll user in course
            from app.services.enrollment_service import EnrollmentService
            try:
                EnrollmentService.enroll_user(db, user_id, course_id)
            except Exception as e:
                # Log error but don't fail the webhook
                print(f"Auto-enrollment failed: {e}")
            
            # Send payment confirmation email
            from app.tasks.email_tasks import send_payment_confirmation_email
            user = db.query(User).filter(User.id == user_id).first()
            course = db.query(Course).filter(Course.id == course_id).first()
            
            if user and course:
                send_payment_confirmation_email(
                    user.email,
                    f"{user.first_name} {user.last_name}",
                    course.title,
                    float(payment.amount)
                )
    
    @staticmethod
    def _handle_payment_succeeded(db: Session, payment_intent: Dict[str, Any]) -> None:
        """Handle successful payment intent."""
        # Additional payment success handling if needed
        pass
    
    @staticmethod
    def _handle_payment_failed(db: Session, payment_intent: Dict[str, Any]) -> None:
        """Handle failed payment intent."""
        payment_id = payment_intent.get('id')
        
        payment = db.query(Payment).filter(
            Payment.stripe_payment_id == payment_id
        ).first()
        
        if payment:
            payment.status = PaymentStatus.FAILED
            db.commit()
    
    @staticmethod
    def get_payment_by_id(db: Session, payment_id: str) -> Payment:
        """
        Get payment by ID.
        
        Args:
            db: Database session
            payment_id: Payment ID
            
        Returns:
            Payment: Payment object
            
        Raises:
            HTTPException: If payment not found
        """
        payment = db.query(Payment).filter(Payment.id == payment_id).first()
        
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Payment not found"
            )
        
        return payment
    
    @staticmethod
    def get_user_payments(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Payment]:
        """
        Get user's payment history.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Payment]: List of payments
        """
        return db.query(Payment).filter(
            Payment.user_id == user_id
        ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_user_payments(db: Session, user_id: str) -> int:
        """
        Count user's payments.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            int: Total payment count
        """
        return db.query(Payment).filter(Payment.user_id == user_id).count()
    
    @staticmethod
    def get_course_payments(
        db: Session,
        course_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Payment]:
        """
        Get payments for a course (Instructor/Admin only).
        
        Args:
            db: Database session
            course_id: Course ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Payment]: List of payments
        """
        return db.query(Payment).filter(
            Payment.course_id == course_id,
            Payment.status == PaymentStatus.COMPLETED
        ).order_by(Payment.paid_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_course_payments(db: Session, course_id: str) -> int:
        """
        Count course payments.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            int: Total payment count
        """
        return db.query(Payment).filter(
            Payment.course_id == course_id,
            Payment.status == PaymentStatus.COMPLETED
        ).count()
    
    @staticmethod
    def get_course_revenue(db: Session, course_id: str) -> Decimal:
        """
        Get total revenue for a course.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            Decimal: Total revenue
        """
        from sqlalchemy import func
        
        total = db.query(func.sum(Payment.amount)).filter(
            Payment.course_id == course_id,
            Payment.status == PaymentStatus.COMPLETED
        ).scalar()
        
        return total or Decimal('0.00')
    
    @staticmethod
    def verify_payment_access(payment: Payment, user: User) -> None:
        """
        Verify that user has access to payment record.
        
        Args:
            payment: Payment object
            user: User object
            
        Raises:
            HTTPException: If user doesn't have access
        """
        from app.models.user import UserRole
        
        if user.role == UserRole.ADMIN:
            return
        
        if payment.user_id != user.id:
            # Check if user is course instructor
            if payment.course and payment.course.instructor_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this payment"
                )
