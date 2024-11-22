from level import Level
from cells import Cell
from state import State
from game import Game
3
levels = [
    Level([
        ['⚫', '⚫', '⚫', '⚫'],
        ['⚫', '⚪', '🔵', '⚪'],
        ['🟣', '⚫', '⚫', '⚫']
    ], 5),
    Level([
        ['⚫', '⚫', '⚪', '⚫', '⚫'],
        ['⚫', '⚫', '🔵', '⚫', '⚫'],
        ['⚪', '🔵', '⚪', '🔵', '⚪'],
        ['⚫', '⚫', '🔵', '⚫', '⚫'],
        ['🟣', '⚫', '⚪', '⚫', '⚫']
    ], 5),
    Level([
        ['🔵', '⚪', '⚪', '⚪', '🔵'],
        ['🔳', '🔳', '🔴', '🔳', '🔳']
    ], 1),
    
]


def display_levels():
    for i, level in enumerate(levels, start=1):
        print(f"Level {i}:\n{level}")


def get_user_choice():
    while True:
        choice = int(input(f"Select a level (1-{len(levels)}): ")) - 1
        if 0 <= choice < len(levels):
            return choice
        else:
            print("Invalid choice, please select a valid level number.")


def main():
    display_levels()
    level_choice = get_user_choice()
    selected_level = levels[level_choice]
    # Convert level grid into a Cell board
    rows = len(selected_level.level_grid)
    columns = len(selected_level.level_grid[0])  # من اول سطر
    board = [[None for _ in range(columns)] for _ in range(rows)]

    for i in range(rows):
        for j in range(columns):
            symbol = selected_level.level_grid[i][j]
            if symbol == '🔳':
                cell_type = 'Out'
            elif symbol == '⚫':
                cell_type = 'Space'
            elif symbol == '🔵':
                cell_type = 'Iron'
            elif symbol == '⚪':
                cell_type = 'White'
            elif symbol == '🔴':
                cell_type = 'Red'
            elif symbol == '🟣':
                cell_type = 'Purple'
            elif symbol == '🔘':
                cell_type = 'WhiteIron'
            elif symbol == '🟥':
                cell_type = 'WhiteRed'
            elif symbol == '🟪':
                cell_type = 'WhitePurple'
            board[i][j] = Cell(i, j, cell_type)

    initial_state = State(rows, columns, board, cost=0)
    print(initial_state)
    game = Game(initial_state)
    game.ucs_play()
    # game.bfs_play()
    # game.dfs_play()
    # game.play(initial_state)
    # print(initial_state)

#     ]
#     rows = len(initial_grid)
#     columns = len(initial_grid[0])
#     board = [[None for _ in range(columns)] for _ in range(rows)]

#     for i in range(rows):
#         for j in range(columns):
#             symbol = initial_grid[i][j]


#             if symbol == '🔳':
#                 cell_type = 'Out'             elif symbol == '⚫':
#                 cell_type = 'Space'
#             elif symbol == '🔵':
#                 cell_type = 'Iron'
#             elif symbol == '⚪':
#                 cell_type = 'White'
#             elif symbol == '🔴':
#                 cell_type = 'Red'
#             elif symbol == '🟣':
#                 cell_type = 'Purple'
#             elif symbol == '🔘':
#                 cell_type = 'WhiteIron'
#             elif symbol == '🟥':
#                 cell_type = 'WhiteRed'
#             elif symbol == '🟪':
#                 cell_type = 'WhitePurple'
#             board[i][j] = Cell(i, j, cell_type)
#     initial_state = State(rows, columns, board)
#     print(initial_state)
#     game = LogicMagnets(initial_state)
#    # game.move()
#    # game.checkMove('Red', 1, 1)  # Attempt to move red magnet to position (1,1)
#    # game.checkMove('Purple', 2, 1)  # Attempt to move purple magnet to position (2,1)
#     game.play()
#     print(initial_state)  # Print the updated board state
if __name__ == "__main__":
    main()
