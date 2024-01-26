import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, User

class Username(AbstractUser):

  username = models.CharField(max_length=50, unique=True)

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = []

  def __str__(self) -> str:
    return self.username


class Puzzle(models.Model):

  puzzle = models.CharField(max_length=81)
  solution = models.CharField(max_length=81)
  difficulty = models.CharField(max_length=100, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])


class Room(models.Model):
  
  id = models.CharField(max_length=6, primary_key=True, default=uuid.uuid4, editable=False)
  user = models.ForeignKey(Username, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  difficulty = models.CharField(max_length=6, choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
  private = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  eligible_points = models.CharField(max_length=81, default='')
  puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE, null=True)
  status = models.CharField(max_length=10, choices=[('ongoing', 'Ongoing'), ('finished', 'Finished')], default='ongoing')
  winner = models.ForeignKey(Username, on_delete=models.CASCADE, null=True, related_name='winner')

  def generate_eligible_points(self):
    self.eligible_points = ''.join(['9' if item == '.' else '0' for item in self.puzzle.puzzle])

  class Meta:
    ordering = ['-created_at']
    

class Board(models.Model):

  player = models.ForeignKey(Username, on_delete=models.CASCADE)
  room = models.ForeignKey(Room, on_delete=models.CASCADE)
  initial_board = models.CharField(max_length=81, default='')
  current_board = models.CharField(max_length=81, default='')
  score = models.IntegerField(default=0)
  active = models.BooleanField(default=True)
  tiles_left = models.SmallIntegerField(default=81)
  
  def save(self, *args, **kwargs):
    self.tiles_left = list(self.current_board).count('.')

    super().save(*args, **kwargs)
  