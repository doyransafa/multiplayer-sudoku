import random
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic.edit import FormView

from sudoku.forms import RoomCreateForm, RegistrationForm
from .consumers import RoomConsumer
from .models import Board, Puzzle, Room, User
from .forms import RoomCreateForm

from . import sudoku

from django_celery_beat.models import PeriodicTask, IntervalSchedule

@login_required(login_url="/login/")
def home(request):

  public_rooms = Room.objects.filter(private=False, status='ongoing')
  active_rooms = Room.objects.filter(user=request.user, status='ongoing')
  
  context = {
    'public_rooms' : public_rooms,
    'active_rooms' : active_rooms,
  }

  return render(request, 'index.html', context)


@login_required(login_url="/login/")
def create_room(request):

  if request.method == 'POST':
    unique_code = RoomConsumer.generate_unique_code()
    form = RoomCreateForm(request.POST)
    if form.is_valid():
      selected_difficulty = form.cleaned_data['difficulty']
      puzzles = Puzzle.objects.filter(difficulty=selected_difficulty)
      random_index = random.randint(0, puzzles.count() - 1)
      random_puzzle = puzzles[random_index]
      room = form.save(commit=False)
      room.user = request.user
      room.id = unique_code
      room.puzzle = random_puzzle
      room.save()
      
      room.generate_eligible_points()
      room.save(update_fields=['eligible_points'])

      interval, _ = IntervalSchedule.objects.get_or_create(every=24, period=IntervalSchedule.HOURS)

      delete_task = PeriodicTask.objects.create(name=f'{unique_code}-delete-task', interval=interval, task='sudoku.tasks.delete_room_after_24_hours' , args=json.dumps([unique_code]), one_off=True)

      return redirect(f'/room/{unique_code}')
  else:
    form = RoomCreateForm()

  context = {'form':form}

  return render(request, 'create_room.html', context)

@login_required(login_url="/login/")
def join_room(request, room_name):

  room = get_object_or_404(Room, id = room_name)
  board = room.puzzle.puzzle

  board_obj, created = Board.objects.get_or_create(player = request.user, room=room)
  all_boards = Board.objects.filter(room=room)
  if created:
    board_obj.initial_board = board
    board_obj.current_board = board
    board_obj.active = True
    board_obj.save()

  current_board = sudoku.board_with_eligibility_info(board_obj.current_board, room.eligible_points, room.puzzle.puzzle)

  context = {
    'room' : room,
    'board' : current_board,
    'all_boards' : all_boards,
    'eligible_points' : room.eligible_points,
  }

  return render(request, 'room.html', context)


def check_tile(request, room_name, col, row, value):

  room = Room.objects.get(id = room_name)

  solved_board = room.puzzle.solution

  board = Board.objects.get(player = request.user, room = room)

  value_index = col * 9 + row
  if board.current_board[value_index] == '.':
    result = solved_board[value_index] == value

    if result:
      board.current_board = update_string(board.current_board, value_index, value)
      eligible_points = int(room.eligible_points[value_index])
      if eligible_points != 1:
        points_rewarded = eligible_points + 1
        remaining_eligible_points = eligible_points - 3
        room.eligible_points = update_string(room.eligible_points, value_index, str(remaining_eligible_points))
        room.save(update_fields=['eligible_points'])
      else:
        points_rewarded = 1
      board.score += points_rewarded
    else:
      board.score -= 10
    
    board.save()

    if board.tiles_left == 0 and board.score > 0:
      room.winner = request.user
      room.status = 'finished'
      room.save()
      
  else:
    result = 'Tile is already solved'

  response = {
    'result' : result,
    'username' : request.user.username,
    'score' : board.score,
    'tiles_left' : board.tiles_left,
  }

  return JsonResponse(response)


def update_string(string:str, index:int, value:str):

  string_list = list(string)
  string_list[index] = value
  return ''.join(string_list)


class RegistrationView(FormView):
  model = User
  template_name = 'registration/register.html'
  form_class = RegistrationForm
  success_url = reverse_lazy('home')

  def form_valid(self, form):
    user = form.save()
    login(self.request, user)
    return super().form_valid(form)


#Error pages

def error_404(request, exception):
  return render(request, 'error_pages/404.html', status=404)

def error_500(request):
  return render(request, 'error_pages/500.html')