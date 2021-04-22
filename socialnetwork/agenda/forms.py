from django import forms

class AgendaCreateForm(forms.Form):
    Title = forms.CharField(label='Title', max_length=100)
    Text = forms.CharField(label ='Text',max_length=255,widget=forms.Textarea)

class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=20)
    password = forms.CharField(label ='password',max_length=30)

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=20)
    email = forms.EmailField(label='email')
    password1 = forms.CharField(label ='password1',max_length=30)
    password2 = forms.CharField(label ='password2',max_length=30)

class AyeCommentForm(forms.Form):
    comment = forms.CharField(label ='comment',max_length=255,widget=forms.Textarea)

class NayCommentForm(forms.Form):
    comment = forms.CharField(label ='comment',max_length=255,widget=forms.Textarea)
