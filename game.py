from cells import Cell
from level import Level
from state import State


class Game:  
    def __init__(self, initial_state) -> None:
        self.initial_state = initial_state
        # self.allstates = [initial_state.copy()]

    def checkSuccess(self):
        for row in self.initial_state.board:
            for cell in row:
                if cell.type == 'White':
                    return False
        return True

    def checkMove(self, magnet_type, target_x, target_y):
        if target_x < 0 or target_x >= self.initial_state.rows or target_y < 0 or target_y >= self.initial_state.columns:
            print("Move out of bounds!")
            return False

        target_cell = self.initial_state.board[target_x][target_y]
        if target_cell.type not in ['Space', 'White']:
            print("Not Allowed Cell To Move!")
            return False
        current_coords = self.initial_state.getMagnetCoords(magnet_type)
        if current_coords is None:
            return False 
        current_x, current_y = current_coords
        current_cell = self.initial_state.board[current_x][current_y]
        #Move
        if target_cell.type == 'Space':
            target_cell.type = magnet_type
        elif target_cell.type == 'White':
            target_cell.type = f'White{magnet_type}'

        # Update the original
        if current_cell.type == f'White{magnet_type}':
            current_cell.type = 'White'
        else:
            current_cell.type = 'Space'

        # Push or Pull if Possible
        self.checkRepelOrAttract(magnet_type, target_x, target_y)
        self.allstates.append(self.initial_state.copy())
        print(f"Moved {magnet_type} to ({target_x}, {target_y})")
        return True

    def getUserMove(self):
        valid_magnets = ['Red', 'Purple', 'WhiteRed', 'WhitePurple']
        magnet_type = input(f"Enter magnet type to move ({
                            ', '.join(valid_magnets)}): ").strip()
        if magnet_type not in valid_magnets:
            print("Invalid magnet type!")
            return False
        try:
            target_x = int(input("Enter target row: ").strip())
            target_y = int(input("Enter target column: ").strip())
        except ValueError:
            print("Invalid coordinates!")
            return False
        if not self.checkMove(magnet_type, target_x, target_y):
            print("Move failed. Please try again.")
        else:
            print("Move successful!")
            print(self.initial_state)
            if self.checkSuccess():
                return True

    def checkRepelOrAttract(self, magnet_type, new_x, new_y):
        if magnet_type == "Purple" or magnet_type == 'WhitePurple':
            self.repelMagnet(new_x, new_y)
        elif magnet_type == "Red" or magnet_type == 'WhiteRed':
            self.attractMagnet(new_x, new_y)
        print(self.initial_state)

    def repelMagnet(self, x, y):
        for j in range(self.initial_state.columns):  # row
            if j != y:
                self.repelCell(x, j)
        for i in range(self.initial_state.rows):  # column
            if i != x:
                self.repelCell(i, y)

    def repelCell(self, x, y):
        cell = self.initial_state.board[x][y]
        if cell.type in ['Iron', 'Red', 'WhiteIron', 'WhiteRed', 'WhitePurple']:
            if cell.type == 'Iron':
                if self.isAdjacentToWhite(x, y):
                    cell.type = 'Space'
                    adjacent_white_cell = self.getAdjacentWhiteCell(x, y)
                    if adjacent_white_cell:
                        adjacent_white_cell.type = 'WhiteIron'
                    print(
                        f"Cell at ({x}, {y}) repelled and merged into WhiteIron.")
                # else:
                #     cell.type = 'Space'
                #     adjacent_white_cell.type == 'Iron'

            elif cell.type == 'Red':
                if self.isAdjacentToWhite(x, y):
                    cell.type = 'Space'
                    adjacent_white_cell = self.getAdjacentWhiteCell(x, y)
                    if adjacent_white_cell:
                        adjacent_white_cell.type = 'WhiteRed'
                    print(
                        f"Cell at ({x}, {y}) repelled and merged into WhiteRed.")
                # else:
                #     cell.type = 'Space'  # No merge, just clear the cell

    def attractMagnet(self, x, y):
        for j in range(self.initial_state.columns):
            if j != y:
                self.pullCell(x, j, x, y)
        for i in range(self.initial_state.rows):
            if i != x:
                self.pullCell(i, y, x, y)

    def pullCell(self, target_x, target_y, magnet_x, magnet_y):
        # target cell to check
        cell = self.initial_state.board[target_x][target_y]
        if cell.type in ['Iron', 'Purple', 'WhiteIron', 'WhitePurple']:
            # Check vertical U-D
            if target_x < magnet_x:
                if target_x + 1 < self.initial_state.rows:  # down
                    next_cell = self.initial_state.board[target_x + 1][target_y]
                    if next_cell.type == 'White':
                        if cell.type == 'WhiteIron' or cell.type == 'WhitePurple':
                            next_cell.type = cell.type
                            cell.type = cell.type.replace('White', '')
                        next_cell.type = f'White{cell.type}'
                        cell.type = 'Space'
                    elif next_cell.type == 'Space':
                        if cell.type in ['WhiteIron', 'WhitePurple']:
                            next_cell = cell.type.replace('White', '')
                            cell.type = 'White'
                        next_cell.type = cell.type
                        cell.type = 'Space'

            elif target_x > magnet_x:
                # up
                if target_x - 1 >= 0:
                    next_cell = self.initial_state.board[target_x - 1][target_y]
                    if next_cell.type == 'White':
                        if cell.type == 'WhiteIron' or cell.type == 'WhitePurple':
                            next_cell.type = cell.type
                            cell.type = cell.type.replace('White', '')
                        next_cell.type = f'White{cell.type}'
                        cell.type = 'Space'
                    elif next_cell.type == 'Space':
                        if cell.type in ['WhiteIron', 'WhitePurple']:
                            next_cell = cell.type.replace('White', '')
                            cell.type = 'White'
                        next_cell.type = cell.type
                        cell.type = 'Space'

            # Check horizontal L-R
            if target_y < magnet_y:
                if target_y + 1 < self.initial_state.columns:  # R
                    next_cell = self.initial_state.board[target_x][target_y + 1]
                    if next_cell.type == 'White':
                        if cell.type == 'WhiteIron' or cell.type == 'WhitePurple':
                            next_cell.type = cell.type
                            cell.type = cell.type.replace('White', '')
                        next_cell.type = f'White{cell.type}'
                        cell.type = 'Space'
                    elif next_cell.type == 'Space':
                        if cell.type in ['WhiteIron', 'WhitePurple']:
                            next_cell = cell.type.replace('White', '')
                            cell.type = 'White'
                        next_cell.type = cell.type
                        cell.type = 'Space'
            elif target_y > magnet_y:
                if target_y - 1 >= 0:  # L
                    next_cell = self.initial_state.board[target_x][target_y - 1]
                    if next_cell.type == 'White':
                        if cell.type == 'WhiteIron' or cell.type == 'WhitePurple':
                            next_cell.type = cell.type
                            cell.type = cell.type.replace('White', '')
                        next_cell.type = f'White{cell.type}'
                        cell.type = 'Space'
                    elif next_cell.type == 'Space':
                        if cell.type in ['WhiteIron', 'WhitePurple']:

                            next_cell = cell.type.replace('White', '')
                            cell.type = 'White'
                        next_cell.type = cell.type
                        cell.type = 'Space'
            else:
                print(f"Cell at ({target_x}, {
                      target_y}) cannot move closer to the magnet.")

    def isAdjacentToWhite(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.initial_state.rows and 0 <= ny < self.initial_state.columns:
                adjacent_cell = self.initial_state.board[nx][ny]
                if adjacent_cell.type == 'White':
                    return True
        return False

    def getAdjacentWhiteCell(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.initial_state.rows and 0 <= ny < self.initial_state.columns:
                adjacent_cell = self.initial_state.board[nx][ny]
                if adjacent_cell.type == 'White':
                    return adjacent_cell
        return None

    def getNeighbourCell(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.initial_state.rows and 0 <= ny < self.initial_state.columns:
                neighbour = self.initial_state.board[nx][ny]
                return neighbour
        return None

    #!.............................................⚡

    def play(self):
        while True:
            self.getUserMove()
            if self.checkSuccess():
                print("WINNNNNNNNNNNN!!")
                break
    

