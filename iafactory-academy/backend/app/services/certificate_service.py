"""
Certificate service for certificate generation and management.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import hashlib
import secrets

from app.models.payment import Certificate
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.course import Course
from app.models.user import User


class CertificateService:
    """Certificate management service."""
    
    @staticmethod
    def generate_certificate_code() -> str:
        """
        Generate unique certificate verification code.
        
        Returns:
            str: Verification code
        """
        # Generate random bytes and create hash
        random_bytes = secrets.token_bytes(16)
        hash_object = hashlib.sha256(random_bytes)
        return hash_object.hexdigest()[:16].upper()
    
    @staticmethod
    def create_certificate(
        db: Session,
        enrollment_id: str
    ) -> Certificate:
        """
        Create certificate for completed enrollment.
        
        Args:
            db: Database session
            enrollment_id: Enrollment ID
            
        Returns:
            Certificate: Created certificate
            
        Raises:
            HTTPException: If enrollment not found or not completed
        """
        enrollment = db.query(Enrollment).filter(
            Enrollment.id == enrollment_id
        ).first()
        
        if not enrollment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Enrollment not found"
            )
        
        if enrollment.status != EnrollmentStatus.COMPLETED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Course must be completed to generate certificate"
            )
        
        # Check if certificate already exists
        existing_certificate = db.query(Certificate).filter(
            Certificate.enrollment_id == enrollment_id
        ).first()
        
        if existing_certificate:
            return existing_certificate
        
        # Generate certificate
        certificate = Certificate(
            user_id=enrollment.user_id,
            course_id=enrollment.course_id,
            enrollment_id=enrollment_id,
            certificate_code=CertificateService.generate_certificate_code(),
            issued_at=datetime.utcnow(),
        )
        
        db.add(certificate)
        db.commit()
        db.refresh(certificate)
        
        # Send certificate notification email
        from app.tasks.email_tasks import send_certificate_notification_email
        user = enrollment.user
        course = enrollment.course
        
        if user and course:
            certificate_url = f"https://iafactory-academy.com/certificates/{certificate.certificate_code}"
            send_certificate_notification_email(
                user.email,
                f"{user.first_name} {user.last_name}",
                course.title,
                certificate_url
            )
        
        return certificate
    
    @staticmethod
    def get_certificate_by_id(db: Session, certificate_id: str) -> Certificate:
        """
        Get certificate by ID.
        
        Args:
            db: Database session
            certificate_id: Certificate ID
            
        Returns:
            Certificate: Certificate object
            
        Raises:
            HTTPException: If certificate not found
        """
        certificate = db.query(Certificate).filter(
            Certificate.id == certificate_id
        ).first()
        
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        
        return certificate
    
    @staticmethod
    def get_certificate_by_code(db: Session, certificate_code: str) -> Certificate:
        """
        Get certificate by verification code.
        
        Args:
            db: Database session
            certificate_code: Certificate code
            
        Returns:
            Certificate: Certificate object
            
        Raises:
            HTTPException: If certificate not found
        """
        certificate = db.query(Certificate).filter(
            Certificate.certificate_code == certificate_code
        ).first()
        
        if not certificate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certificate not found"
            )
        
        return certificate
    
    @staticmethod
    def verify_certificate(db: Session, certificate_code: str) -> dict:
        """
        Verify certificate authenticity.
        
        Args:
            db: Database session
            certificate_code: Certificate code
            
        Returns:
            dict: Certificate verification details
        """
        certificate = CertificateService.get_certificate_by_code(db, certificate_code)
        
        user = db.query(User).filter(User.id == certificate.user_id).first()
        course = db.query(Course).filter(Course.id == certificate.course_id).first()
        
        return {
            'valid': True,
            'certificate_code': certificate.certificate_code,
            'issued_at': certificate.issued_at,
            'user_name': f"{user.first_name} {user.last_name}" if user else "Unknown",
            'user_email': user.email if user else None,
            'course_title': course.title if course else "Unknown",
            'course_instructor': f"{course.instructor.first_name} {course.instructor.last_name}" if course and course.instructor else "Unknown"
        }
    
    @staticmethod
    def get_user_certificates(
        db: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Certificate]:
        """
        Get user's certificates.
        
        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Certificate]: List of certificates
        """
        return db.query(Certificate).filter(
            Certificate.user_id == user_id
        ).order_by(Certificate.issued_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_user_certificates(db: Session, user_id: str) -> int:
        """
        Count user's certificates.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            int: Total certificate count
        """
        return db.query(Certificate).filter(Certificate.user_id == user_id).count()
    
    @staticmethod
    def get_course_certificates(
        db: Session,
        course_id: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[Certificate]:
        """
        Get certificates for a course (Instructor/Admin only).
        
        Args:
            db: Database session
            course_id: Course ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List[Certificate]: List of certificates
        """
        return db.query(Certificate).filter(
            Certificate.course_id == course_id
        ).order_by(Certificate.issued_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def count_course_certificates(db: Session, course_id: str) -> int:
        """
        Count course certificates.
        
        Args:
            db: Database session
            course_id: Course ID
            
        Returns:
            int: Total certificate count
        """
        return db.query(Certificate).filter(Certificate.course_id == course_id).count()
    
    @staticmethod
    def generate_certificate_pdf(certificate: Certificate, user: User, course: Course) -> bytes:
        """
        Generate certificate PDF (placeholder for actual PDF generation).
        
        Args:
            certificate: Certificate object
            user: User object
            course: Course object
            
        Returns:
            bytes: PDF file content
            
        Note:
            This is a placeholder. Actual implementation would use a PDF library
            like ReportLab or weasyprint to generate a professional certificate.
        """
        # TODO: Implement actual PDF generation with ReportLab or similar
        
        # Placeholder PDF content
        pdf_content = f"""
        Certificate of Completion
        
        This certifies that
        {user.first_name} {user.last_name}
        
        has successfully completed the course
        {course.title}
        
        Issued on: {certificate.issued_at.strftime('%B %d, %Y')}
        Certificate Code: {certificate.certificate_code}
        
        Instructor: {course.instructor.first_name} {course.instructor.last_name}
        
        Verify at: https://iafactory-academy.com/verify/{certificate.certificate_code}
        """.encode('utf-8')
        
        return pdf_content
    
    @staticmethod
    def delete_certificate(db: Session, certificate: Certificate) -> None:
        """
        Delete certificate.
        
        Args:
            db: Database session
            certificate: Certificate object
        """
        db.delete(certificate)
        db.commit()
    
    @staticmethod
    def verify_certificate_access(certificate: Certificate, user: User) -> None:
        """
        Verify that user has access to certificate.
        
        Args:
            certificate: Certificate object
            user: User object
            
        Raises:
            HTTPException: If user doesn't have access
        """
        from app.models.user import UserRole
        
        if user.role == UserRole.ADMIN:
            return
        
        if certificate.user_id != user.id:
            # Check if user is course instructor
            course = certificate.course
            if not course or course.instructor_id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to access this certificate"
                )
