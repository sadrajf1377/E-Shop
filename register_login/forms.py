from django import forms


class register_form(forms.Form):
    full_name=forms.CharField(label='نام و نام خانوادگی',max_length=20,required=True,widget=forms.TextInput(attrs={'class':'register_form'}))
    email=forms.EmailField(label='ایمیل شما',max_length=100,required=True,widget=forms.EmailInput(attrs={'class':'register_form'}))
    password=forms.CharField(label='رمز عبور',max_length=60,required=True,widget=forms.PasswordInput(attrs={'class':'register_form'}))
    password_repeat=forms.CharField(label='تکرار رمز عبور',max_length=60,required=True,widget=forms.PasswordInput(attrs={'class':'register_form'}))
