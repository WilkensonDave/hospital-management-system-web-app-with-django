from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauthentication.models import User


USER_TYPE =(
    ("patient", "patient"),
    ('doctor', "doctor")
)

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"Full Name"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"example@gmail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Enter password here.."}))
    # password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Confirm Password"}))
    user_type = forms.ChoiceField(choices=USER_TYPE, widget=forms.Select(attrs={"class":"form-select"}))
   
    class Meta:
        model = User
        fields = ['full_name', "email", "password1", "password2", "user_type"]
    
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':"example@gmail.com"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':"Enter password here.."}))

    # class Meta:
    #     model = User
    #     fields = ["email", "password1"]
    
    # def __init__(self, *args, **kwargs):
    #     super(UserLoginForm, self).__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs.update({'class':'form-control'})