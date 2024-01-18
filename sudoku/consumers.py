import json
import random
import string
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class RoomConsumer(WebsocketConsumer):
    
  def connect(self):
    from .models import Room, Board
    self.room_group_name = self.scope['url_route']['kwargs']['room_name']
    self.user = self.scope.get('user')
    self.player_board = Board.objects.get(player = self.user, room__id=self.room_group_name) 
    self.room = Room.objects.get(id = self.room_group_name) 
    self.player_score = self.player_board.score
    self.player_board.active = True
    self.player_board.save()

    # if self.room.status == 'ongoing':
    async_to_sync(self.channel_layer.group_add)(
      self.room_group_name,
      self.channel_name
    )
    
    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name, {
        'type' : 'player_entered_exited',
        'event' : 'player_entered',
        'username': self.user.username,
        'player_score': self.player_score, 
      })

    self.accept()
  
  def disconnect(self, code):
    from .models import Board
    self.user = self.scope.get('user')
    self.player_board = Board.objects.get(player = self.user, room__id=self.room_group_name)
    self.player_board.active = False
    self.player_board.save()

    async_to_sync(self.channel_layer.group_send)(
      self.room_group_name, {
        'type' : 'player_entered_exited',
        'event' : 'player_exited',
        'username': self.user.username,
      }
      )

    return super().disconnect(code)
  
  def receive(self, text_data=None, bytes_data=None):
    text_data_json = json.loads(text_data)
    message_type = text_data_json.get('type')
    username = text_data_json.get('username')

    if message_type == 'chat_message':
      message = text_data_json.get('message')
      async_to_sync(self.channel_layer.group_send)(
        self.room_group_name, {
          'type' : 'send_chat_message',
          'username': username,
          'message': message,
        })
    elif message_type == 'guess':
      tile = text_data_json.get('tile')
      score = text_data_json.get('score')
      result = text_data_json.get('result')
      tiles_left = text_data_json.get('tiles_left')
      async_to_sync(self.channel_layer.group_send)(
        self.room_group_name, {
          'type' : 'send_guess',
          'result': result,
          'username': username,
          'tile': tile,
          'score': score,
          'tiles_left': tiles_left,
        })

  def player_entered_exited(self, event):
    username = event.get('username')
    event_type = event.get('event')
    player_score = event.get('player_score', '')
    self.send(text_data=json.dumps({
      'type' : event_type,
      'username': username,
      'player_score': player_score,
    }))

  def send_chat_message(self, event):

    username = event.get('username')
    message = event.get('message')

    self.send(text_data=json.dumps({
      'type' : 'chat_message',
      'username': username,
      'message': message,
    }))

  def send_guess(self, event):
    username = event.get('username')
    tile = event.get('tile')
    score = event.get('score')
    result = event.get('result')
    tiles_left = event.get('tiles_left')

    self.send(text_data=json.dumps({
      'type' : 'guess',
      'result' : result,
      'username': username,
      'tile': tile,
      'score': score,
      'tiles_left': tiles_left,
    }))

  @staticmethod
  def generate_unique_code(length=6):
    # Generate a unique room code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
