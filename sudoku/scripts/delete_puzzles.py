from ..models import Puzzle

def run():
  # Fetch all puzzles
  puzzles = Puzzle.objects.all()
  # Delete puzzles
  puzzles.delete()