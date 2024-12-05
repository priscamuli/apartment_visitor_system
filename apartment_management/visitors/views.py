from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import ResidentRegisterForm, ReceptionistRegisterForm
from .models import  Visitor
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import VisitorForm
from django.contrib import messages

def is_receptionist(user):
    return user.groups.filter(name='Receptionist').exists()

def is_resident(user):
    return user.groups.filter(name='Resident').exists()

def resident_register(request):
    if request.method == 'POST':
        form = ResidentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to the login page
    else:
        form = ResidentRegisterForm()

    return render(request, 'resident_register.html', {'form': form})


def receptionist_register(request):
    if request.method == 'POST':
        form = ReceptionistRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Receptionist registration successful. You can now log in.")
            return redirect('login')  # Redirect to the login page
    else:
        form = ReceptionistRegisterForm()

    return render(request, 'receptionist_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a success page
                return redirect('dashboard')  # Adjust to the appropriate view name
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('login')


@login_required
def dashboard(request):
    visitors = Visitor.objects.all()
    return render(request, 'dashboard.html', {'visitors': visitors})

@login_required()
def visitor_create(request):
    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.added_by = request.user
            visitor.save()
            return redirect('dashboard')  # Redirect to the dashboard or any other page
    else:
        form = VisitorForm()

    return render(request, 'visitor_create.html', {'form': form})

@login_required()
@user_passes_test(is_receptionist)
def visitor_update(request,pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if request.method == 'POST':
        form = VisitorForm(request.POST, instance=visitor)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = VisitorForm(instance=visitor)
    return render(request, 'visitor_form.html', {'form': form})

@login_required()
@user_passes_test(is_receptionist)
def visitor_delete(request,pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    if request.method == 'POST':
        visitor.delete()
        return request('dashboard')
    return render(request,'delete_confirmation.html', {'visitor': visitor})


#search visitors records view
@login_required
def search_visitors(request):
    query = request.GET.get('q', '')
    results = Visitor.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results})

@login_required
@user_passes_test(is_receptionist)
def visitor_check_out(request, pk):
    visitor = get_object_or_404(Visitor, pk=pk)
    visitor.check_out = timezone.now()
    visitor.save()
    return redirect('dashboard')