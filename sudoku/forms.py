from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class RoomCreateForm(forms.ModelForm):
  DIFFICULTY_CHOICES = [
      ('easy', 'Easy'),
      ('medium', 'Medium'),
      ('hard', 'Hard'),
  ]
  
  difficulty = forms.ChoiceField(
    choices=DIFFICULTY_CHOICES,
    widget=forms.RadioSelect(attrs={'class': 'flex'}),
    initial='easy'
  )

  class Meta:
    model = Room
    fields = ['name','difficulty', 'private']
  

class RegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username','email']