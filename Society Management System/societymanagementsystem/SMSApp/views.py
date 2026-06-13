from urllib import request

from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Count

# Create your views here.
from .models import ServiceRequest, Announcement , HouseUser

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        house_number = request.POST.get('house_number')
        phone_number = request.POST.get('phone_number')
        
        try:
            # Check if email already exists
            if HouseUser.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': 'Email already exists'})
            
            # Hash the password before saving
            hashed_password = make_password(password)
            
            # Create and save the user
            user = HouseUser.objects.create(
                name=name, 
                email=email, 
                house_number=house_number,
                phone_number=phone_number, 
                password=hashed_password,
                is_active=False
            )
            link = f"http://127.0.0.1:8000/activate/{user.id}/"
            user.save()
            
            # Send activation email
            try: 
                from django.core.mail import send_mail
                send_mail(
                    'Activate Your Account',
                    f'Click the link to activate your account: {link}',
                    'ranamazhar214@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return HttpResponse("Registration successful! Please check your email to activate your account.")
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"Email Error: {error_details}")  # Log to console for debugging
                return render(request, 'register.html', {'error': f'Failed to send activation email: {str(e)}'})

            # Redirect to login page after successful registration
            return redirect('login')
        except Exception as e:
            return render(request, 'register.html', {'error': f'Registration failed: {str(e)}'})
    
    return render(request, 'register.html')

def login(request):

    if request.session.get("user_id"):
        return redirect("dashboard")

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Get user by email
            user = HouseUser.objects.get(email=email)
            
            # Check if account is activated
            if not user.is_active:
                return render(
                    request,
                    "login.html",
                    {"error": "Please activate your account via the activation link sent to your email"}
                )
            
            # Check if password matches using Django's check_password
            if check_password(password, user.password):
                # Save user_id to session
                request.session["user_id"] = user.id
                request.session["user_name"] = user.name
                request.session["user_email"] = user.email

                print("LOGIN SUCCESS")
                print("SESSION USER ID =", request.session.get("user_id"))
                
                return redirect("dashboard")
            else:
                return render(
                    request,
                    "login.html",
                    {"error": "Invalid Email or Password"}
                )

        except HouseUser.DoesNotExist:
            return render(
                request,
                "login.html",
                {"error": "Invalid Email or Password"}
            )
    
    return render(request, "login.html")
def dashboard(request):
     user_id = request.session.get("user_id")

     if not user_id:
        return redirect("login")

     user = HouseUser.objects.get(id=user_id)

     total_requests = ServiceRequest.objects.filter(
        user=user
    ).count()

     pending_requests = ServiceRequest.objects.filter(
        user=user,
        status="PENDING"
    ).count()

     approved_requests = ServiceRequest.objects.filter(
        user=user,
        status="APPROVED"
    ).count()
      
     total_announcements = Announcement.objects.count()

     requests = ServiceRequest.objects.filter(user=user).order_by("-created_at")[:5]
     

     context = {
        "total_requests": total_requests,
        "pending_requests": pending_requests,
        "approved_requests": approved_requests,
        "total_announcements": total_announcements,
        "requests": requests,
        "user": user
    }

     return render(
        request,
        "dashboard.html",
        context
    )

def create_request(request):
    user_id = request.session.get("user_id")
    user = HouseUser.objects.get(id=user_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        ServiceRequest.objects.create(
            user_id=request.session.get('user_id'),
            title=title,
            description=description,
            category=category
        )
        return redirect('dashboard')
    
    return render(request, 'create_request.html')

def view_requests(request):
    user_id = request.session.get("user_id")
    user = HouseUser.objects.get(id=user_id)
    requests = ServiceRequest.objects.filter(user=user).order_by("-created_at")[:5]
    return render(request, 'view_requests.html', {'requests': requests})
    
def edit_request(request, request_id):
    user_id = request.session.get("user_id")
    user = HouseUser.objects.get(id=user_id)
    service_request = get_object_or_404(
        ServiceRequest,
        id=request_id
    )

    if request.method == "POST":

        service_request.title = request.POST.get("title")
        service_request.category = request.POST.get("category")
        service_request.description = request.POST.get("description")

        service_request.save()

        return redirect("view_requests")
    return render(request, 'edit_request.html', {'request': service_request})

def delete_request(request, request_id):
    user_id = request.session.get("user_id")
    user = HouseUser.objects.get(id=user_id)
    request_obj = ServiceRequest.objects.get(id=request_id, user=user)
    request_obj.delete()
    return redirect('view_requests')

def announcements(request):
    announcements = Announcement.objects.all().order_by(
        "-created_at"
    )
    return render(
        request,
        "announcements.html",
        {
            "announcements": announcements
        }
    )

def logout(request):
    # Clear session
    request.session.flush()
    return redirect('login')

def admin_login(request):
    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        if email == "admin@gmail.com" and password == "admin123":

            request.session["admin"] = True

            return redirect("admin_dashboard")

        else:

            return render(
                request,
                "admin_login.html",
                {
                    "error":"Invalid Admin Credentials"
                }
            )

    return render(request,"admin_login.html")

def admin_dashboard(request):

    if not request.session.get("admin"):

        return redirect("admin_login")

    return render(
        request,
        "admin_dashboard.html"
    )

from .models import *

def admin_dashboard(request):

    if not request.session.get("admin"):
        return redirect("admin_login")

    context = {

        "total_users": HouseUser.objects.count(),

        "total_requests": ServiceRequest.objects.count(),

        "pending_requests":
        ServiceRequest.objects.filter(
            status="PENDING"
        ).count(),

        "approved_requests":
        ServiceRequest.objects.filter(
            status="APPROVED"
        ).count(),

        "completed_requests":
        ServiceRequest.objects.filter(
            status="COMPLETED"
        ).count(),

        "total_announcements":
        Announcement.objects.count(),
    }

    return render(
        request,
        "admin_dashboard.html",
        context
    )

def manage_requests(request):

    if not request.session.get("admin"):
        return redirect("admin_login")

    requests = ServiceRequest.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "manage_requests.html",
        {
            "requests": requests
        }
    )

def approve_request(request,id):

    req = ServiceRequest.objects.get(id=id)

    req.status = "APPROVED"

    req.save()

    return redirect("manage_requests")

def complete_request(request,id):

    req = ServiceRequest.objects.get(id=id)

    req.status = "COMPLETED"

    req.save()

    return redirect("manage_requests")

def delete_request_admin(request,id):

    req = ServiceRequest.objects.get(id=id)

    req.delete()

    return redirect("manage_requests")

def manage_announcements(request):

    if not request.session.get("admin"):
        return redirect("admin_login")

    if request.method == "POST":

        title = request.POST.get("title")
        message = request.POST.get("message")

        Announcement.objects.create(
            title=title,
            message=message
        )

        return redirect("manage_announcements")

    announcements = Announcement.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "announcements_manage.html",
        {
            "announcements": announcements
        }
    )

def delete_announcement(request,id):

    announcement = Announcement.objects.get(
        id=id
    )

    announcement.delete()

    return redirect(
        "manage_announcements"
    )



def manage_users(request):

    if not request.session.get("admin"):
        return redirect("admin_login")

    search = request.GET.get("search")

    users = HouseUser.objects.all()

    if search:
        users = users.filter(
            name__icontains=search
        )

    user_data = []

    for user in users:

        total_requests = ServiceRequest.objects.filter(
            user=user
        ).count()

        user_data.append({
            "user": user,
            "total_requests": total_requests
        })

    context = {
        "user_data": user_data
    }

    return render(
        request,
        "manage_users.html",
        context
    )

def delete_user(request,id):

    user = HouseUser.objects.get(id=id)

    user.delete()

    return redirect("manage_users")

def admin_logout(request):
    # Clear session
    request.session.flush()
    return redirect('admin_login')



def send_email_to_all_users(request):
    """Admin function to send emails to all users"""
    if not request.session.get("admin"):
        return redirect("admin_login")
    
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if not subject or not message:
            return render(request, 'send_email.html', {'error': 'Subject and message are required'})
        
        # Get all active users
        users = HouseUser.objects.filter(is_active=True)
        email_list = [user.email for user in users]
        
        if not email_list:
            return render(request, 'send_email.html', {'error': 'No active users to send emails to'})
        
        try:
            from django.core.mail import send_mail
            result = send_mail(
                subject=subject,
                message=message,
                from_email='ranamazhar214@gmail.com',
                recipient_list=email_list,
                fail_silently=False,
            )
            
            success_message = f'Email successfully sent to {len(email_list)} user(s)!'
            return render(request, 'send_email.html', {
                'success': success_message,
                'user_count': len(email_list)
            })
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Email Error: {error_details}")
            return render(request, 'send_email.html', {'error': f'Failed to send email: {str(e)}'})
    
    # GET request - show the form
    user_count = HouseUser.objects.filter(is_active=True).count()
    return render(request, 'send_email.html', {'user_count': user_count})

def activate_account(request, user_id):
    
    user = get_object_or_404(HouseUser, id=user_id)
    if user.is_active == False:
      user.is_active = True
      user.save()
      return redirect('login')
    else:
      return HttpResponse("Account is already active.")

import uuid

from django.core.mail import send_mail
from django.conf import settings
def forget_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = HouseUser.objects.get(
                email=email
            )

            token = str(uuid.uuid4())

            user.reset_token = token
            user.save()

            reset_link = (
                f"http://127.0.0.1:8000/"
                f"reset_password/{token}/"
            )

            send_mail("Password Reset",f"""Hello {user.name}
                      Click below link to reset password:
                      {reset_link}""",
                      settings.EMAIL_HOST_USER,
                      [user.email],
                      fail_silently=False
            )

            return redirect("password_reset_done")

        except HouseUser.DoesNotExist:

            return render(request,"forget_password.html",{"error":"Email not found"}
            )

    return render(request,"forget_password.html")  

def password_reset_done(request):

    return render(request,"password_reset_done.html")


def reset_password(request, token):
    
    from django.contrib.auth.hashers import make_password

    try:

        user = HouseUser.objects.get(reset_token=token)

    except HouseUser.DoesNotExist:

        return render(request,"invalid_token.html")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return render(request,"reset_password.html",{"error":"Passwords do not match"})
        user.password = make_password(password)
        user.reset_token = None
        user.save()
        return redirect("password_reset_complete")

    return render(request,"reset_password.html")  

def password_reset_complete(request):

    return render(request,"password_reset_complete.html")