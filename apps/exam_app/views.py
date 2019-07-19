from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Job
import bcrypt
import re


def index(request):
    return render(request, "exam_app/login.html")
#REGISTER WITH VALIDATIONS IN MODELS
def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
        request.session['user'] = new_user.id
        return redirect('/dashboard')
#LOGIN WITH LOGIN VALIDATIONS

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        l_email = User.objects.get(email=request.POST['email'])
        l_password = request.POST['password']
        passwords_match = bcrypt.checkpw(
            l_password.encode(), l_email.password.encode())
        if passwords_match:
            request.session['user'] = l_email.id
            return redirect('/dashboard')
        else:
            return redirect('/')
#SUCCESSFULLY LOGGED IN / REGISTERED
def dashboard(request):
    if not 'user' in request.session:
        messages.error(request, "You must log in.")
        return redirect('/')
    else:
        users = {
            'user': User.objects.get(
                id=request.session['user']),
            'job': Job.objects.all(),
        }
        print(request.session['user'])
        return render(request, 'exam_app/dashboard.html', users)


def jobs_id(request, id):
    current_job = Job.objects.get(id=id)
    user = {
        'user': User.objects.get(
            id=request.session['user']),
        'job': current_job
    }
    return render(request, 'exam_app/view_job.html', user)

def job(request):
    user = {
        'user': User.objects.get(
            id=request.session['user']),
    }
    return render(request, 'exam_app/add_job.html', user)

def add_job(request):
    errors = Job.objects.job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/job')
    else:
        current_user = User.objects.get(id=request.session['user'])
        new_job = Job.objects.create(
            title=request.POST['title'], description=request.POST['description'], location=request.POST['location'],category=request.POST['category'], uploaded_by=current_user)
        return redirect('/dashboard')

def edit(request, id):
    current_job = Job.objects.get(id=id)
    user = {
        'user': User.objects.get(
            id=request.session['user']),
        'job': current_job
    }
    return render(request, 'exam_app/edit_job.html', user)

def edit_job(request, id):
    errors = Job.objects.edit_job_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/jobs/edit/{id}')
    else:
        job_to_update = Job.objects.get(id=id)
        job_to_update.title = request.POST['title']
        job_to_update.description = request.POST['description']
        job_to_update.location = request.POST['location']
        job_to_update.category = request.POST['category']
        job_to_update.save()
        return redirect(f'/jobs/{id}')

def delete_job(request, id):
    job_to_delete = Job.objects.get(id=id)
    job_to_delete.delete()
    return redirect('/dashboard')


def add_favorites(request, id):
    current_job = Job.objects.get(id=id)
    current_user = User.objects.get(id=request.session['user'])
    user = {
        'user': User.objects.get(
            id=request.session['user']),
        'book': current_job
    }
    current_job.users_who_like.add(current_user)
    return redirect(f'/jobs/{id}')


def remove_favorites(request, id):
    current_job = Job.objects.get(id=id)
    current_user = User.objects.get(id=request.session['user'])
    user = {
        'user': User.objects.get(id=request.session['user']),
        'book': current_job
    }
    current_job.users_who_like.remove(current_user)
    return redirect(f'/jobs/{id}')
#LOGOUT
def logout(request):
    request.session.clear()
    return redirect('/')
