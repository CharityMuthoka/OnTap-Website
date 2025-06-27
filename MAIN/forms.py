from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)



class NameForm(forms.Form):
    full_name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label="Your email", max_length=100)


class JobForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    company = forms.CharField(label='Company', max_length=100)

class PhotoForm(forms.Form):
    profile_pic = forms.ImageField(label='Upload your photo')

class ContactForm(forms.Form):
    email = forms.EmailField()
    phone = forms.CharField(label='Phone', max_length=15)

    from django import forms

class RegisterForm(forms.Form):
    fullname = forms.CharField(max_length=100,required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


    
