from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import Http404
from .froms import UserForm
from .models import User
import logging

# Set up logging
logger = logging.getLogger(__name__)

# This function will add new student and show all student.
def addshow(request):
    """
    Handle adding new students and displaying all students.
    Includes comprehensive exception handling.
    """
    try:
        if request.method == 'POST':
            fm = UserForm(request.POST)
            if fm.is_valid():
                try:
                    name = fm.cleaned_data['name']
                    email = fm.cleaned_data['email']
                    password = fm.cleaned_data['password']
                    
                    # Check if user with same email already exists
                    if User.objects.filter(email=email).exists():
                        messages.error(request, f'User with email {email} already exists!')
                        return render(request, 'enroll/addandshow.html', {'form': fm, 'stu': User.objects.all()})
                    
                    reg = User(name=name, email=email, password=password)
                    reg.save()
                    messages.success(request, f'Student {name} added successfully!')
                    return redirect('addshow')
                    
                except IntegrityError as e:
                    logger.error(f"Database integrity error: {e}")
                    messages.error(request, 'Database error occurred. Please try again.')
                except Exception as e:
                    logger.error(f"Unexpected error in form processing: {e}")
                    messages.error(request, 'An unexpected error occurred. Please try again.')
            else:
                # Form validation failed
                messages.error(request, 'Please correct the errors below.')
        else:
            fm = UserForm()
            
        # Get all students for display
        stud = User.objects.all()
        return render(request, 'enroll/addandshow.html', {'form': fm, 'stu': stud})
        
    except Exception as e:
        logger.error(f"Critical error in addshow view: {e}")
        messages.error(request, 'A system error occurred. Please try again later.')
        return render(request, 'enroll/addandshow.html', {'form': UserForm(), 'stu': []})

# This function will update/edit the student information.
def update(request, id):
    """
    Handle updating student information.
    Includes comprehensive exception handling.
    """
    try:
        # Get the user object or return 404
        pi = get_object_or_404(User, pk=id)
        
        if request.method == 'POST':
            fm = UserForm(request.POST, instance=pi)
            if fm.is_valid():
                try:
                    # Check if email is being changed and if it conflicts with existing users
                    new_email = fm.cleaned_data['email']
                    if new_email != pi.email and User.objects.filter(email=new_email).exists():
                        messages.error(request, f'User with email {new_email} already exists!')
                        return render(request, 'enroll/updatestudent.html', {'form': fm})
                    
                    fm.save()
                    messages.success(request, f'Student {pi.name} updated successfully!')
                    return redirect('addshow')
                    
                except IntegrityError as e:
                    logger.error(f"Database integrity error in update: {e}")
                    messages.error(request, 'Database error occurred. Please try again.')
                except Exception as e:
                    logger.error(f"Unexpected error in update processing: {e}")
                    messages.error(request, 'An unexpected error occurred. Please try again.')
            else:
                messages.error(request, 'Please correct the errors below.')
        else:
            fm = UserForm(instance=pi)
            
        return render(request, 'enroll/updatestudent.html', {'form': fm})
        
    except Http404:
        messages.error(request, 'Student not found!')
        return redirect('addshow')
    except Exception as e:
        logger.error(f"Critical error in update view: {e}")
        messages.error(request, 'A system error occurred. Please try again later.')
        return redirect('addshow')

# This function will delete the student information.
def delete(request, id):
    """
    Handle deleting student information.
    Includes comprehensive exception handling.
    """
    try:
        if request.method == 'POST':
            # Get the user object or return 404
            pi = get_object_or_404(User, pk=id)
            
            try:
                student_name = pi.name  # Store name before deletion for message
                pi.delete()
                messages.success(request, f'Student {student_name} deleted successfully!')
                return redirect('addshow')
                
            except IntegrityError as e:
                logger.error(f"Database integrity error in delete: {e}")
                messages.error(request, 'Cannot delete student due to database constraints.')
                return redirect('addshow')
            except Exception as e:
                logger.error(f"Unexpected error in delete processing: {e}")
                messages.error(request, 'An unexpected error occurred while deleting.')
                return redirect('addshow')
        else:
            # If not POST request, redirect to addshow
            messages.warning(request, 'Invalid request method for deletion.')
            return redirect('addshow')
            
    except Http404:
        messages.error(request, 'Student not found!')
        return redirect('addshow')
    except Exception as e:
        logger.error(f"Critical error in delete view: {e}")
        messages.error(request, 'A system error occurred. Please try again later.')
        return redirect('addshow')
