from django import forms

class AgendaCreateForm(forms.Form):
    Title = forms.CharField(label='Title', max_length=100)
    Text = forms.CharField(label ='Text',max_length=255,widget=forms.Textarea)