from django.shortcuts import render

from .forms import NameForm, JobForm, PhotoForm, ContactForm, RegisterForm
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Card
from django import forms
import requests
from django.contrib import messages
from django.views.decorators.cache import never_cache

from django.contrib.messages import get_messages






def index(request):
    return render(request, 'index.html')


def shop(request):
    return render(request, 'shop.html', {'title': 'Shop'})

def pricing(request):
    return render(request, 'pricing.html', {'title': 'Pricing'})

def about_us(request):
    return render(request, 'about_us.html', {'title': 'About_us'})

def contact(request):
    return render(request, 'contact.html', {'title': 'Contact'})

def our_team(request):
    return render(request, 'our_team.html')

def crm_integrations(request):
    return render(request,'crm_integrations.html')

def our_journey(request):
    return render(request, 'our_journey.html')

def success(request):
    return render(request, 'success.html')

def solutions(request):
    return render(request, 'solutions.html', {'title': 'Solutions'})

def resources(request):
    return render(request, 'resources.html', {'title': 'Resources'})


@never_cache
def dashboard(request):
    if not request.session.get('email'):
        messages.error(request, "Session expired or not logged in. Please sign in again.")
        return redirect('sign_in')

    email = request.session.get('email')
    fullname = request.session.get('fullname', '')

    return render(request, 'webapp Signin/dashboard.html', {
        'email': email,
        'fullname': fullname
    })





def logout(request):
    request.session.flush() 
    messages.success(request, "You have been logged out successfully.")

    return redirect('sign_in')



def choose_account_type(request):
    return render(request, 'registration/choose_account_type.html')

def register_individual(request):
    return render(request, 'registration/register_individual.html')

def enter_password(request):
    return render(request, 'registration/enter_password.html')

def otp_verification(request):
    return render(request,'webapp Registration/otp_verification.html')
    



def choose_otp_method(request):
    if request.method == 'POST':
        method = request.POST.get('method')
        destination = None

        if method == 'email':
            destination = request.POST.get('destination_email')
        elif method == 'phone':
            raw_phone = request.POST.get('destination_phone')
            country_code='+254'

            if raw_phone:
                # Ensure no leading 0
                if raw_phone.startswith('0'):
                    raw_phone = raw_phone[1:]
                elif raw_phone.startswith('254'):
                   raw_phone = raw_phone[3:]
                elif raw_phone.startswith('+254'):
                   raw_phone = raw_phone[4:]


                # Always prefix with +254
                destination = f"+254{raw_phone}"
                request.session['country_code'] = '+254'
            else:
                messages.error(request, "Please enter a valid phone number.")
                return redirect('choose_otp_method')

        else:
            messages.error(request, "Please select where to receive the verification code.")
            return redirect('choose_otp_method')

        acc_id = request.session.get("acc_id")

        if not acc_id or not destination:
            messages.error(request, "Missing account ID or contact information.")
            return redirect('register_account')

        #  Store for later use in OTP verification
        request.session['otp_method'] = method
        request.session['otp_destination'] = destination

        # Attempt to send the OTP
        payload = {
            "method": method,
            "destination": destination,
            "acc_id": acc_id
        }

        try:
            response = requests.post(
                'https://dev.ontapke.com/acc/api/delivery-method/',
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            print("OTP Response Code:", response.status_code)
            print("OTP Raw Response:", response.text)

            if response.status_code == 200:
                messages.success(request, f"OTP sent successfully to your {method}.")
                return redirect('enter_otp')
            else:
                messages.error(request, "Failed to send OTP. Please try again.")
                return redirect('choose_otp_method')

        except requests.exceptions.RequestException as e:
            print("Delivery method API error:", e)
            messages.error(request, "Network error. Please try again later.")
            return redirect('choose_otp_method')

    return render(request, 'webapp Registration/choose_otp_method.html')

   

from django.shortcuts import render, redirect
from django.contrib import messages




def enter_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        method = request.session.get('otp_method')
        destination = request.session.get('otp_destination')
        acc_id = request.session.get('acc_id')
        from_registration = request.session.get('from_registration', False)

        if not method or not destination or not otp or not acc_id:
            messages.error(request, "Missing OTP or session info.")
            return redirect('choose_otp_method')

        #  REGISTER - Verify email only
        if from_registration:
            try:
                email_verify_response = requests.post(
                    'https://dev.ontapke.com/acc/api/verify-email/',
                    json={"acc_id": acc_id, "otp": otp},
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                email_verify_json = email_verify_response.json()
                print("Email Verify Response:", email_verify_response.status_code, email_verify_json)

                message_value = email_verify_json.get("message", "")
                if isinstance(message_value, list):
                    message_value = message_value[0]

                if email_verify_response.status_code == 200:
                    messages.success(request, "Email verified. You can now sign in.")
                    return redirect('sign_in')

                elif isinstance(message_value, str) and "already verified" in message_value.lower():
                    messages.info(request, "Account already verified. Please log in.")
                    return redirect('sign_in')

                else:
                    messages.error(request, message_value or "Email verification failed.")
                    return redirect('enter_otp')

            except requests.exceptions.RequestException as e:
                print("Email Verification Error:", e)
                messages.error(request, "Network error during email verification.")
                return redirect('enter_otp')

        # LOGIN - Verify OTP only
        else:
            try:
                otp_response = requests.post(
                    'https://dev.ontapke.com/acc/api/verify-otp/',
                    json={
                        "method": method,
                        "destination": destination,
                        "otp": otp,
                        "acc_id": acc_id
                    },
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )
                otp_json = otp_response.json()
                print("OTP Verification Response:", otp_response.status_code, otp_json)

                if otp_response.status_code == 200:
                    user_data = otp_json.get('data', {}).get('user', {})
                    request.session['acc_id'] = user_data.get('acc_id')
                    request.session['email'] = user_data.get('email')
                    request.session['phone'] = user_data.get('phone')

                    messages.success(request, "Login successful.")
                    return redirect('dashboard')

                else:
                    error_msg = otp_json.get('message') or otp_json.get('otp', ["Invalid or expired OTP."])[0]
                    messages.error(request, error_msg)
                    return redirect('enter_otp')

            except requests.exceptions.RequestException as e:
                print("OTP VERIFY Error:", e)
                messages.error(request, "Network error during OTP verification.")
                return redirect('enter_otp')

    #return render(request, 'webapp Registration/otp_verification.html')
    return render(request, 'webapp Registration/otp_verification.html', {
    'otp_method': request.session.get('otp_method'),
    'destination': request.session.get('otp_destination'),
})



def resend_otp(request):
    email = request.session.get('email')
    acc_id = request.session.get('acc_id')

    if not email or not acc_id:
        messages.error(request, "Account ID or email not found in session. Please sign in again.")
        return redirect('sign_in')

    payload = {
        "email": email,
        "acc_id": acc_id
    }

    try:
        response = requests.post(
            "https://dev.ontapke.com/acc/api/resend-verification/",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        if response.status_code == 200:
            messages.success(request, "Verification code resent. Check your email.")
        else:
            try:
                data = response.json()
                messages.error(request, data.get("message", "Failed to resend code."))
            except ValueError:
                messages.error(request, "Unexpected response from server.")

    except requests.exceptions.RequestException as e:
        print("Resend OTP Error:", e)
        messages.error(request, "Network error. Try again later.")

    return redirect('enter_otp')

def otp_error(request):
    return render(request, 'webapp Registration/otp_error.html')





def invalid_otp(request):
    return render(request, 'webapp Registration/invalid_otp.html')

def register_business(request):
    return render(request, 'registration/register_business.html')

def register_account(request):
    return render(request, 'webapp Registration/register_account.html')



import requests
from django.contrib import messages
from django.shortcuts import render, redirect

@never_cache


def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        payload = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(
                'https://dev.ontapke.com/acc/api/login/',
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            data = response.json()
            print("Login Response:", data)

            if response.status_code == 200:
                # verified
                acc_id = data.get("acc_id")
                if isinstance(acc_id, list):
                    acc_id = acc_id[0]

                request.session['acc_id'] = acc_id
                request.session['email'] = email

                messages.success(request, "Signed in successfully.")
                return redirect('dashboard')

            elif response.status_code == 400:
                #Handle verification
                if data.get("requires_verification", ["False"])[0] == "True":
                    acc_id = data.get("acc_id", [""])[0]

                    request.session['acc_id'] = acc_id
                    request.session['email'] = email
                    request.session['otp_method'] = 'email'
                    request.session['otp_destination'] = email

                    messages.info(request, "Please verify your email to continue.")
                    return redirect('choose_otp_method')

                #  Login failed 
                messages.error(request, data.get("message", ["Login failed."])[0])

            else:
                messages.error(request, "Login failed. Please check your credentials.")

        except requests.exceptions.RequestException as e:
            print("Network Error:", e)
            messages.error(request, "Network error. Try again later.")

    return render(request, 'webapp Signin/sign_in.html')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        payload = {
            "method": "email",
            "destination": email
        }

        try:
            response = requests.post(
                'https://dev.ontapke.com/acc/api/forgot-password/',
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            print(" OTP Status:", response.status_code)
            print(" Response:", response.text)

            if response.status_code in [200, 201]:
                request.session['reset_email'] = email
                messages.success(request, "OTP sent to your email.")
                return redirect('verify_otp')
            else:
                messages.error(request, "Failed to send OTP.")

        except requests.exceptions.RequestException:
            messages.error(request, "Network error.")
    
    return render(request, 'webapp Signin/forgot_password.html')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.session.get('email') or request.session.get('reset_email')


        payload = {
            "otp": otp,
            "destination": email
        }

        print("DEBUG: Verifying OTP", otp, "for", email)
       

        try:
            response = requests.post(
                'https://dev.ontapke.com/acc/api/verify-otp/',
                json=payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                messages.success(request, "OTP verified.")
                return redirect('reset_password')
            else:
                messages.error(request, "Invalid OTP.")

        except:
            messages.error(request, "Something went wrong.")

    return render(request, 'webapp Registration/verify_otp.html')





def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        email = request.session.get('reset_email')

        payload = {
            "destination": email,
            "new_password": new_password
        }

        try:
            response = requests.post(
                'https://dev.ontapke.com/acc/api/reset-password/',
                json=payload,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                messages.success(request, "Password updated. You can now sign in.")
                return redirect('sign_in')
            else:
                messages.error(request, "Reset failed.")

        except:
            messages.error(request, "Something went wrong.")

    return render(request, 'webapp Signin/reset_password.html')


def success(request):
    return render(request, 'webapp Signin/success.html')



def register_account(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country_code')
        password = request.POST.get('password')

        # Normalize phone format
        if phone.startswith('0'):
            phone = phone[1:]
        if not country_code.startswith('+'):
            country_code = f"+{country_code}"

        full_phone = f"{country_code}{phone}"

        payload = {
            "fullname": fullname,
            "email": email,
            "phone": full_phone,
            "password": password
        }

        try:
            response = requests.post(
                'https://dev.ontapke.com/acc/api/register/',
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            try:
                data = response.json()
            except ValueError:
                data = {}

            print("Status Code:", response.status_code)
            print("Raw Response:", response.text)

            if response.status_code == 201:
                user_data = data.get("data", {}).get("user", {})

                acc_id = user_data.get("acc_id")
                request.session['acc_id'] = acc_id
                request.session['email'] = email
                request.session['phone'] = full_phone  

                #  Cache locally
                RegisteredUser.objects.get_or_create(
                    acc_id=acc_id,
                    defaults={
                        "email": email,
                        "phone": full_phone
                    }
                )

                messages.success(request, "Account registered successfully. Please verify your email/phone.")
                return redirect('choose_otp_method')

            elif response.status_code == 400 and isinstance(data, dict):
                for field, messages_list in data.items():
                    if isinstance(messages_list, list):
                        for msg in messages_list:
                            messages.error(request, f"{field.capitalize()}: {msg}")
                    elif isinstance(messages_list, dict):
                        nested_msg = messages_list.get("message")
                        if nested_msg:
                            messages.error(request, f"{field.capitalize()}: {nested_msg}")

        except requests.exceptions.RequestException as e:
            print("Network Exception:", e)
            messages.error(request, "Network error. Please try again later.")

    return render(request, 'webapp Registration/register_account.html')


from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            instance=form.save()
            # Get data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # email data
            subject = f"New message from {name} via OnTap Contact Form"
            message_body = f"From: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Sending the email
            send_mail(
                subject,
                message_body,
                email,  
                ['youremail@example.com'], 
                fail_silently=False,
            )

            return redirect('success')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})




class OtpChoiceForm(forms.Form):
    method = forms.ChoiceField(choices=[('email', 'Email'), ('phone', 'Phone')], widget=forms.RadioSelect)


from .models import RegisteredUser





from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import RegisteredUser

def register_user(request):
    if request.method == "POST":
        acc_id = request.POST["acc_id"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        username = request.POST["username"]
        password = request.POST["password"]

        
        user = User.objects.create_user(username=username, email=email, password=password)

        
        RegisteredUser.objects.get_or_create(
            acc_id=acc_id,
            defaults={
                "email": email,
                "phone": phone
            }
        )

        return redirect("signin")  
    return render(request, "webapp Registration/register_account.html")


