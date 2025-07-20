from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import cloudinary
import cloudinary.uploader
import cloudinary.api
from cloudinary.forms import CloudinaryFileField
from .models import Post, Category,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','status', 'section', 'content', 'image', 'category']

class RegisterForm(forms.Form):
    image = CloudinaryFileField(required=False)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data  

class Loginform(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, label="Your Password", required=True)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email or not password:
            return cleaned_data  # Stop here if fields are missing, default validation will handle it.

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            self.add_error('email', "No such email registered.")
            return cleaned_data

        user = authenticate(username=user.username, password=password)
        if user is None:
            self.add_error('password', "Invalid email or password.")  # Attach error to password field

        cleaned_data['user'] = user  # Store authenticated user in cleaned_data
        return cleaned_data
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")