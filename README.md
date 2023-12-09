
# Multiplayer Sudoku With Django Websockets

## Features

- Login/Logout/Register
- Create public or private rooms.
- Attend rooms and play realtime Sudoku with other users.
- Live chat with users in same room.

## Video Demo
### [YouTube Link]( https://youtu.be/9Xtj5zKnvnM )

<img width="721" alt="image" src="https://github.com/doyransafa/multiplayer-sudoku/assets/72417108/e6f1a861-c24b-4be1-a153-05b3562ba50a">


## Build Steps

Create a virtual environment

    python -m venv /path/to/new/virtual/environment

Activate virtual environment  
MacOS:

    source venv/bin/activate

for Windows PowerShell

    <venv_path>\Scripts\Activate.ps1  

Install dependencies 

    pip install -r requirements.txt

Migrate database  

    python manage.py makemigrations
    python manage.py migrate

Create admin user. Needed if you want to use Admin dashboard.

    python manage.py createsuperuser

Start server, port number is optional, default is 8000

    python manage.py runserver 8080
