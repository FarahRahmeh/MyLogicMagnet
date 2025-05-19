from level import Level
from cells import Cell
from state import State
from game import Game

levels = [
    Level([
        ['⚫', '⚫', '⚫', '⚫'],
        ['⚫', '⚪', '🔵', '⚪'],
        ['🟣', '⚫', '⚫', '⚫']
    ]),
    Level([
        ['⚫', '⚫', '⚪', '⚫', '⚫'],
        ['⚫', '⚫', '🔵', '⚫', '⚫'],
        ['⚪', '🔵', '⚪', '🔵', '⚪'],
        ['⚫', '⚫', '🔵', '⚫', '⚫'],
        ['🟣', '⚫', '⚪', '⚫', '⚫']
    ]),
    Level([
        ['🔵', '⚪', '⚪', '⚪', '🔵'],
        ['🔳', '🔳', '🔴', '🔳', '🔳']
    ]),
    # Level([['⚪', '🔵', '⚪', '🔵', '⚫'],
    #        ['⚫', '⚫', '🟣', '⚫', '⚪'],
    #        ['⚫', '⚫', '🔴', '⚫', '⚪'],
    #        ])

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
            print("select a valid level number")


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

    initial_state = State(rows, columns, board, cost=0, heurstic=0)
    print(initial_state)
    game = Game(initial_state)
    # game.ucs_play()
    # game.hill_climbing_play()
    game.a_star_play()
    # game.bfs_play()
    # game.dfs_play()
    # game.play(initial_state)
    # print(initial_state)


if __name__ == "__main__":
    main()
