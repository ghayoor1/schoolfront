from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateUserForm, LoginForm, AddRecordForm, UpdateRecordForm, AddContactForm, FriendRequestForm, ImageForm
from django.contrib.auth.models import auth, User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from . models import Customer, Contact, FriendRequest, Image
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
    image= Image.objects.all()
    context = {'records':record , 'images' : image}
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


# Sending a Friend Request

@login_required(login_url='my-login')
def add_contact(request):
    form = AddContactForm()
    if request.method == "POST":
        form = AddContactForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')

            try:
                recipient = User.objects.get(username=username)

                if recipient == request.user:
                    messages.error(request, "You cannot send a friend request to yourself.")
                    return redirect('add-contact')

                # Check if a friend request already exists
                existing_request = FriendRequest.objects.filter(from_user=request.user, to_user=recipient).exists()

                if existing_request:
                    messages.error(request, "A friend request has already been sent to this user.")
                    return redirect('add-contact')

                # Create a new friend request
                friend_request = FriendRequest(from_user=request.user, to_user=recipient, status='pending')
                friend_request.save()

                messages.success(request, f"Friend request sent to {username}.")
                return redirect('add-contact')

            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
                return redirect('add-contact')
            
    context={'form': form}
    return render(request, 'webapp/add-contact.html', context=context)

# Accepting a Friend Request

@login_required(login_url='my-login')
def accept_friend_request(request, request_id):
    sender_info = {}
    
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user and friend_request.status == 'pending':
        friend_request.status = 'accepted'
        friend_request.save()
        sender = friend_request.from_user
        contact,_ = Contact.objects.get_or_create(user=request.user, username = sender.username)
        contact.save()
        messages.success(request, f"You are now friends with {sender.username}.")
    else:
        messages.error(request, "You are not authorized to accept this friend request.")
    return redirect('view-friend-request')

 # Rejecting a Friend Request

@login_required(login_url='my-login')
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.get(id=request_id)
    if friend_request.to_user == request.user and friend_request.status == 'pending':
        friend_request.status = 'rejected'
        friend_request.save()
        messages.success(request, "Friend request rejected successfully.")
    else:
        messages.error(request, "You are not authorized to reject this friend request.")
    return redirect('view-friend-request')


# Viewing a Friend Request

@login_required(login_url='my-login')
def view_friend_requests(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')

    if request.method == 'POST':
        # This part is for handling form submissions (accept or reject friend requests)
        # It will redirect to the same view after processing the requests
        for friend_request in friend_requests:
            form = FriendRequestForm(instance=friend_request, data=request.POST)
            if form.is_valid():
                if form.cleaned_data['accept']:
                    return redirect('accept-friend-request', request_id=friend_request.id)
                elif form.cleaned_data['reject']:
                    return redirect('reject-friend-request', request_id=friend_request.id)
                

    # Pass the friend requests along with sender names to the template
    friend_requests_data = [(request, request.from_user.username) for request in friend_requests]
    forms = [FriendRequestForm(instance=request) for request in friend_requests]

    context = {'friend_requests_data': friend_requests_data, 'forms': forms}
    return render(request, 'webapp/friend-request.html', context=context)     



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


# - Creating and SUbmitting Image Form

@login_required(login_url='my-login')
def upload_image(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            return redirect ('dashboard')
    context = {'form' : form}
    return render(request, 'webapp/upload-image.html' , context)

# - Adding the functionality for the Like Button

def like_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    if request.user in image.liked_users.all():
        image.liked_users.remove(request.user)
        image.likes -= 1
    else:
        if request.user in image.disliked_users.all():
            image.disliked_users.remove(request.user)
            image.dislikes -= 1
        image.liked_users.add(request.user)
        image.likes += 1
    image.save()
    return redirect('dashboard')

# - Adding the functionality for the Dislike Button

def dislike_image(request, image_id):
    image = Image.objects.get(pk=image_id)
    if request.user in image.disliked_users.all():
        image.disliked_users.remove(request.user)
        image.dislikes -= 1
    else:
        if request.user in image.liked_users.all():
            image.liked_users.remove(request.user)
            image.likes -= 1
        image.disliked_users.add(request.user)        
        image.dislikes += 1
    image.save()
    return redirect('dashboard')


# - Delete the uploaded image

@login_required(login_url='my-login')
def delete_image(request, pk):
    img = get_object_or_404(Image, pk=pk)
    img.delete()
    return redirect('dashboard')

#- logout a user

@login_required(login_url='my-login')
def user_logout(request):
    auth.logout(request)
    return redirect('my-login')




