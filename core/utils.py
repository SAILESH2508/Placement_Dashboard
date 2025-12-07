"""
Utility functions for the placement portal
"""

from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count, Max
from .models import Placement, Student, Company
import logging

logger = logging.getLogger(__name__)


def send_placement_notification(student, company, position, package):
    """
    Send email notification when a student gets placed
    
    Args:
        student: Student instance
        company: Company instance
        position: Job position
        package: Package in LPA
    """
    try:
        subject = f"Congratulations! Placement Offer from {company.name}"
        message = f"""
        Dear {student.user.get_full_name() if student.user else student.roll_no},
        
        Congratulations! You have received a placement offer:
        
        Company: {company.name}
        Position: {position}
        Package: {package} LPA
        
        Please contact the placement cell for further details.
        
        Best regards,
        Placement Cell
        """
        
        recipient_email = student.user.email if student.user else None
        
        if recipient_email:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )
            logger.info(f"Placement notification sent to {recipient_email}")
            return True
        else:
            logger.warning(f"No email found for student {student.roll_no}")
            return False
            
    except Exception as e:
        logger.error(f"Error sending placement notification: {str(e)}")
        return False


def calculate_placement_statistics(year=None, branch=None):
    """
    Calculate comprehensive placement statistics
    
    Args:
        year: Filter by academic year (optional)
        branch: Filter by branch (optional)
    
    Returns:
        dict: Statistics dictionary
    """
    try:
        # Filter students
        students_qs = Student.objects.all()
        if year:
            students_qs = students_qs.filter(year=year)
        if branch:
            students_qs = students_qs.filter(branch=branch)
        
        total_students = students_qs.count()
        
        # Filter placements
        placements_qs = Placement.objects.filter(student__in=students_qs)
        
        # Calculate statistics
        placed_students = placements_qs.values('student').distinct().count()
        total_placements = placements_qs.count()
        
        package_stats = placements_qs.aggregate(
            avg_package=Avg('package_lpa'),
            max_package=Max('package_lpa')
        )
        
        # Top companies
        top_companies = (
            placements_qs.values('company__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        
        return {
            'total_students': total_students,
            'placed_students': placed_students,
            'placement_percentage': round((placed_students / total_students * 100), 2) if total_students > 0 else 0,
            'total_placements': total_placements,
            'average_package': round(float(package_stats['avg_package'] or 0), 2),
            'highest_package': float(package_stats['max_package'] or 0),
            'top_companies': list(top_companies),
        }
        
    except Exception as e:
        logger.error(f"Error calculating statistics: {str(e)}")
        return {}


def validate_student_eligibility(student, min_cgpa=6.0):
    """
    Check if student is eligible for placements
    
    Args:
        student: Student instance
        min_cgpa: Minimum CGPA requirement
    
    Returns:
        tuple: (is_eligible, reason)
    """
    if student.cgpa < min_cgpa:
        return False, f"CGPA below minimum requirement ({min_cgpa})"
    
    if not student.user:
        return False, "No user account linked"
    
    if not student.user.email:
        return False, "Email not configured"
    
    return True, "Eligible"


def get_student_recommendations(student):
    """
    Get company recommendations for a student based on their profile
    
    Args:
        student: Student instance
    
    Returns:
        QuerySet: Recommended companies
    """
    try:
        # Get companies that have hired from the same branch
        branch_placements = Placement.objects.filter(
            student__branch=student.branch
        ).values('company').distinct()
        
        recommended_companies = Company.objects.filter(
            id__in=branch_placements
        ).annotate(
            placement_count=Count('placements')
        ).order_by('-placement_count')[:10]
        
        return recommended_companies
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        return Company.objects.none()


def export_placement_data(queryset, format='csv'):
    """
    Export placement data in various formats
    
    Args:
        queryset: Placement queryset
        format: Export format ('csv', 'json', 'excel')
    
    Returns:
        str: Exported data
    """
    import csv
    import json
    from io import StringIO
    
    if format == 'csv':
        output = StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'Student Roll No', 'Student Name', 'Branch', 'CGPA',
            'Company', 'Position', 'Package (LPA)', 'Date Offered', 'Confirmed'
        ])
        
        # Data
        for placement in queryset.select_related('student', 'student__user', 'company'):
            writer.writerow([
                placement.student.roll_no,
                placement.student.user.get_full_name() if placement.student.user else '',
                placement.student.branch,
                placement.student.cgpa,
                placement.company.name,
                placement.position,
                placement.package_lpa,
                placement.date_offered,
                'Yes' if placement.confirmed else 'No'
            ])
        
        return output.getvalue()
    
    elif format == 'json':
        data = []
        for placement in queryset.select_related('student', 'student__user', 'company'):
            data.append({
                'student_roll_no': placement.student.roll_no,
                'student_name': placement.student.user.get_full_name() if placement.student.user else '',
                'branch': placement.student.branch,
                'cgpa': float(placement.student.cgpa),
                'company': placement.company.name,
                'position': placement.position,
                'package_lpa': float(placement.package_lpa),
                'date_offered': str(placement.date_offered),
                'confirmed': placement.confirmed
            })
        return json.dumps(data, indent=2)
    
    else:
        raise ValueError(f"Unsupported format: {format}")
