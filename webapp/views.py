from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm, AddContactForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Customer, Contact
from django.contrib import messages

# - homepage

def home(request):
    return render(request, "webapp/index.html")

# - register a user

def register(request):

    form= CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('my-login')
    context = {'form':form}
    return render(request, 'webapp/register.html', context=context)

# - login a user

def my_login(request):

    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request, data= request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    context= {'form': form}
    return render(request, 'webapp/my-login.html', context=context)

# - Dashboard
@login_required(login_url='my-login')
def dashboard(request):

    record= Customer.objects.all()
    context = {'records':record}
    return render(request, 'webapp/dashboard.html', context=context)

# - Add Record 
@login_required(login_url='my-login')
def add_record(request):

        form = AddRecordForm()
        if request.method == "POST":
            form = AddRecordForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    
        context= {'form': form}
        return render(request, 'webapp/create-record.html', context=context)

# - Update a Record 
@login_required(login_url='my-login')
def update_record(request,pk):
        record=Customer.objects.get(id=pk)

        form = UpdateRecordForm(instance=record)
        if request.method == "POST":
            form = UpdateRecordForm(request.POST, instance=record)
            if form.is_valid():
                form.save()
                return redirect('dashboard')
    
        context= {'form': form}
        return render(request, 'webapp/update-record.html', context=context)

# - View a Singular Record of the Customer
@login_required(login_url='my-login')
def singular_record(request,pk):
     all_records=Customer.objects.get(id=pk)
     context= {'record':all_records}
     return render(request, 'webapp/view-record.html',context=context)

# - Delete the Singular Record of the Customer
@login_required(login_url='my-login')
def delete_record(request,pk):
     record=Customer.objects.get(id=pk)
     record.delete()
     return redirect('dashboard')

# - Contacts
@login_required(login_url='my-login')
def view_contact(request):
    # Filter contacts based on the currently logged-in user
    contacts = Contact.objects.filter(user=request.user)
    context = {'contacts': contacts}
    return render(request, 'webapp/view-contacts.html', context=context)

# - Add Contact
@login_required(login_url='my-login')
def add_contact(request):
    form = AddContactForm()
    if request.method == "POST":
        form = AddContactForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            try:
                # Check if the user with the given username exists in the User model
                user_to_add = User.objects.get(username=username)
                user = request.user  # Get the currently logged-in user

                # Check if the contact already exists for the logged-in user
                if Contact.objects.filter(user=user, username=username).exists():
                    messages.error(request, f"{username} is already in your contacts.")
                    return redirect('add-contact')

                elif user == user_to_add:  # Prevent adding oneself as a contact
                    messages.error(request, "You cannot add yourself as a contact.")
                    return redirect('add-contact')

                else:
                    # Ensure that the contact is associated with the currently logged-in user
                    Contact.objects.create(user=user, username=username)
                    messages.success(request, f"{username} has been added to your contacts.")
                    return redirect('view-contact')

            except User.DoesNotExist:
                messages.error(request, f"User with username {username} does not exist.")

    context = {'form': form}
    return render(request, 'webapp/add-contact.html', context=context)

# - View a Singular Contact of the Customer
@login_required(login_url='my-login')
def singular_contact(request,pk):
     all_contacts=Contact.objects.get(id=pk)
     context= {'contacts':all_contacts}
     return render(request, 'webapp/single-contact.html',context=context)

# - Delete the Singular Contact of the Customer
@login_required(login_url='my-login')
def delete_contact(request,pk):
     contact=Contact.objects.get(id=pk)
     contact.delete()
     return redirect('view-contact')


#- logout a user

def user_logout(request):
    auth.logout(request)
    return redirect('my-login')




