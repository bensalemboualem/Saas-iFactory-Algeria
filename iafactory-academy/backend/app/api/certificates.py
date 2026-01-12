"""
Certificate API routes for certificate management.
"""
from typing import Annotated
from fastapi import APIRouter, Depends, Response, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io

from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin
from app.models.user import User
from app.schemas.payment import CertificateResponse
from app.schemas.base import PaginationParams, PaginatedResponse
from app.services.certificate_service import CertificateService
from app.services.enrollment_service import EnrollmentService


router = APIRouter()


@router.post("/enrollments/{enrollment_id}/generate", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
def generate_certificate(
    enrollment_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Generate certificate for completed enrollment.
    
    - Course must be 100% completed
    - Certificate is automatically sent via email
    """
    enrollment = EnrollmentService.get_enrollment_by_id(db, enrollment_id)
    EnrollmentService.verify_enrollment_access(enrollment, current_user)
    
    certificate = CertificateService.create_certificate(db, enrollment_id)
    return certificate


@router.get("/my-certificates", response_model=PaginatedResponse[CertificateResponse])
def get_my_certificates(
    pagination: Annotated[PaginationParams, Depends()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get current user's certificates.
    """
    certificates = CertificateService.get_user_certificates(
        db,
        current_user.id,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size
    )
    total = CertificateService.count_user_certificates(db, current_user.id)
    
    return PaginatedResponse(
        items=certificates,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.get("/{certificate_id}", response_model=CertificateResponse)
def get_certificate(
    certificate_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get certificate by ID.
    
    Users can only view their own certificates unless admin.
    """
    certificate = CertificateService.get_certificate_by_id(db, certificate_id)
    CertificateService.verify_certificate_access(certificate, current_user)
    
    return certificate


@router.get("/{certificate_id}/download")
def download_certificate(
    certificate_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Download certificate as PDF.
    
    Returns PDF file for download.
    """
    certificate = CertificateService.get_certificate_by_id(db, certificate_id)
    CertificateService.verify_certificate_access(certificate, current_user)
    
    user = certificate.user
    course = certificate.course
    
    # Generate PDF
    pdf_content = CertificateService.generate_certificate_pdf(certificate, user, course)
    
    # Create response with PDF
    pdf_stream = io.BytesIO(pdf_content)
    
    return StreamingResponse(
        pdf_stream,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=certificate_{certificate.certificate_code}.pdf"
        }
    )


@router.get("/verify/{certificate_code}")
def verify_certificate(
    certificate_code: str,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Verify certificate authenticity (Public endpoint).
    
    - **certificate_code**: Certificate verification code
    
    Returns certificate details if valid.
    """
    verification_data = CertificateService.verify_certificate(db, certificate_code)
    return verification_data


@router.get("/course/{course_id}/certificates", response_model=PaginatedResponse[CertificateResponse])
def get_course_certificates(
    course_id: str,
    pagination: Annotated[PaginationParams, Depends()],
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get certificates for a course (Instructor owner or Admin only).
    """
    from app.services.course_service import CourseService
    course = CourseService.get_course_by_id(db, course_id)
    CourseService.verify_instructor_access(course, current_user)
    
    certificates = CertificateService.get_course_certificates(
        db,
        course_id,
        skip=(pagination.page - 1) * pagination.page_size,
        limit=pagination.page_size
    )
    total = CertificateService.count_course_certificates(db, course_id)
    
    return PaginatedResponse(
        items=certificates,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size,
        pages=(total + pagination.page_size - 1) // pagination.page_size
    )


@router.delete("/{certificate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certificate(
    certificate_id: str,
    current_user: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    Delete certificate (Admin only).
    
    Use with caution - this removes the certificate record.
    """
    certificate = CertificateService.get_certificate_by_id(db, certificate_id)
    CertificateService.delete_certificate(db, certificate)
