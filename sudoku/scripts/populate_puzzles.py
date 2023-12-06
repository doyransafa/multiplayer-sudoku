import csv
from ..models import Puzzle

def run():

  with open('./puzzles.csv', 'r') as file:
    
    csvreader = csv.reader(file)
    header = next(csvreader)
    for index, row in enumerate(csvreader):
      Puzzle.objects.create(puzzle=row[1], solution = row[2], difficulty = row[4])
      print(f'adding row {index + 1}')
