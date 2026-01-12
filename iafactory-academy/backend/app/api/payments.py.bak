"""
Payment API routes for Stripe integration.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.payment import (
    CheckoutSessionCreate,
    CheckoutSessionResponse,
    PaymentResponse,
)
from app.schemas.base import PaginationParams, PaginatedResponse
from app.services.payment_service import PaymentService
from app.services.course_service import CourseService


router = APIRouter()


@router.post("/checkout", response_model=CheckoutSessionResponse, status_code=status.HTTP_201_CREATED)
def create_checkout_session(
    checkout_data: CheckoutSessionCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Create Stripe checkout session for course purchase.
    
    - **course_id**: Course to purchase
    - **success_url**: URL to redirect on successful payment
    - **cancel_url**: URL to redirect on cancelled payment
    
    Returns Stripe checkout session URL.
    """
    course = CourseService.get_course_by_id(db, checkout_data.course_id)
    
    session_data = PaymentService.create_checkout_session(
        db,
        current_user,
        course,
        checkout_data.success_url,
        checkout_data.cancel_url
    )
    
    return CheckoutSessionResponse(**session_data)


@router.post("/webhook", status_code=status.HTTP_200_OK)
async def stripe_webhook(
    request: Request,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Handle Stripe webhook events.
    
    This endpoint receives payment events from Stripe:
    - checkout.session.completed
    - payment_intent.succeeded
    - payment_intent.payment_failed
    
    Automatically enrolls users on successful payment.
    """
    payload = await request.body()
    signature = request.headers.get('stripe-signature')
    
    if not signature:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing Stripe signature"
        )
    
    result = PaymentService.handle_webhook_event(db, payload, signature)
    return result


@router.get("/my-payments", response_model=PaginatedResponse[PaymentResponse])
def get_my_payments(
    pagination: Annotated[PaginationParams, Depends()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get current user's payment history.
    """
    payments = PaymentService.get_user_payments(
        db,
        current_user.id,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size
    )
    total = PaymentService.count_user_payments(db, current_user.id)
    
    return PaginatedResponse(
        items=payments,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get payment by ID.
    
    Users can only view their own payments unless admin.
    """
    payment = PaymentService.get_payment_by_id(db, payment_id)
    PaymentService.verify_payment_access(payment, current_user)
    
    return payment


@router.get("/course/{course_id}", response_model=PaginatedResponse[PaymentResponse])
def get_course_payments(
    course_id: str,
    pagination: Annotated[PaginationParams, Depends()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get payments for a course (Instructor owner or Admin only).
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    payments = PaymentService.get_course_payments(
        db,
        course_id,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size
    )
    total = PaymentService.count_course_payments(db, course_id)
    
    return PaginatedResponse(
        items=payments,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/course/{course_id}/revenue")
def get_course_revenue(
    course_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get total revenue for a course (Instructor owner or Admin only).
    
    Returns total revenue and payment count.
    """
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    revenue = PaymentService.get_course_revenue(db, course_id)
    count = PaymentService.count_course_payments(db, course_id)
    
    return {
        'course_id': course_id,
        'total_revenue': float(revenue),
        'payment_count': count,
        'currency': 'USD'
    }
