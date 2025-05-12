from django import forms
import re
from user_Module.models import normal_user


pattern=r'(?=.*[A-Z].*)(?=.*[0-9].*)'

class register_form(forms.ModelForm):
    class Meta:
        model=normal_user
        fields=['username','email','password']
        labels={'username':'نام کاربری','email':'ایمیل','password':'رمز عبور'}
        widgets={'username':forms.TextInput(),'email':forms.EmailInput(),'password':forms.PasswordInput()}
    password_repeat=forms.CharField(required=True,label='تکرار رمز عبور',widget=forms.PasswordInput())
    def is_valid(self):

        password=self.data.get('password')
        pass_repeat=self.data.get('password_repeat')
        passwords_match=password==pass_repeat
        strong_password=re.match(pattern,password)
        print(strong_password)
        if not passwords_match:
            self.add_error('password_repeat','رمز عبور و تکرار رمز عبور یکی نیستند')
        if not(strong_password):
            self.add_error('password','رمز عبور حداقل باید یک حرف بزرگ،یک عدد   داشته باشد')
        return super().is_valid() and strong_password and passwords_match


class login_form(forms.Form):
    username_email=forms.CharField(max_length=200,label='ایمیل یا نام کاربری',required=True,widget=forms.TextInput(),error_messages={'required':'نام کاربری یا ایمیل را وارد نمایید'})
    password=forms.CharField(widget=forms.PasswordInput(),label='رمز عبور',required=True,error_messages={'required':'رمز عبور را وارد نمایید'})
