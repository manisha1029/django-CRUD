from django.shortcuts import render, redirect
from .froms import UserForm
from .models import User

# Create your views here.
# This function will add new student and show all student.
def addshow(request):
    if request.method == 'POST':
        fm = UserForm(request.POST)
        if fm.is_valid():
            name = fm.cleaned_data['name']
            email = fm.cleaned_data['email']
            password = fm.cleaned_data['password']
            reg = User(name=name, email=email, password=password)
            reg.save()
            return redirect('addshow')
    else:
        fm = UserForm()
    stud = User.objects.all()
    return render(request, 'enroll/addandshow.html', {'form': fm, 'stu': stud})

# This function will update/edit the student information.
def update(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id)
        fm = UserForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()
            return redirect('addshow')
    else:
        pi = User.objects.get(pk=id)
        fm = UserForm(instance=pi)
    return render(request, 'enroll/updatestudent.html', {'form': fm});


# This function will delete the student information.
def delete(request, id):
    if request.method == 'POST':
        pi = User.objects.get(pk=id) # pk is primary key.
        pi.delete()
        return redirect('addshow')
