from django import forms
from .models import Room, Username

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
  

class RegistrationForm(forms.ModelForm):

  class Meta:
    model = Username
    fields = ['username']