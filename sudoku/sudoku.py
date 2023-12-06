def is_valid(board:list[list[int]], col, row, value) -> bool:
  
  for i in range(9):
    if board[row][i] == value:
      return False
    if board[i][col] == value:
      return False
  col_grid = col//3
  row_grid = row//3
  for i in range(row_grid * 3, row_grid * 3 + 3):
    for j in range (col_grid * 3, col_grid * 3 + 3):
      if board[i][j] == value:
        return False
  return True

def solve(board:str) -> str:

  for row in range(9):
    for col in range(9):
      if board[row][col] == 0:
        for possible in range(1,10):
          if is_valid(board, col, row, possible):
            board[row][col] = possible
            if solve(board):
              return stringify_board(board)
            else:
              board[row][col] = 0
        return None    
  return stringify_board(board)

def stringify_board(board:list[list[int]]) -> str:

  str_board = ''
  
  for row in board:
    for digit in row:
      str_board += str(digit)

  return str_board

def str_to_matrix_board(str_board:str) -> list[list[int]]:

  str_board = str_board.replace('.','0')

  matrix_board = []
  for i in range(9):
    start = i * 9
    end = i * 9 + 9
    row = []
    for digit in str_board[start:end]:
      row.append(int(digit))
    matrix_board.append(row)

  return matrix_board

def board_with_eligibility_info(str_board, eligible_points, initial_board):
  
  str_board = str_board.replace('.','0')
  initial_board = initial_board.replace('.','0')

  matrix_board = []
  for i in range(9):
    start = i * 9
    end = i * 9 + 9
    info_dict = []
    for index, digit in enumerate(str_board[start:end]):
      info_dict.append({
        'value' : digit,
        'eligible_points' : eligible_points[start+index],
        'solved_by_player': '1' if initial_board[start+index] != str_board[start+index] else '0',
      })
    matrix_board.append(info_dict)

  return matrix_board

