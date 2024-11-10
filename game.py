from cells import Cell
from level import Level
from state import State
from copy import deepcopy
from collections import deque


class Game:
    def __init__(self, initial_state) -> None:
        self.initial_state = initial_state
        self.current_state = deepcopy(initial_state)
        self.states = [self.initial_state]

    def checkSuccess(self, state):
        for row in state.board:
            for cell in row:
                if cell.type == ('White'):
                    return False
        return True

    def checkMove(self, state, magnet_type, target_x, target_y):
        if target_x < 0 or target_x >= state.rows or target_y < 0 or target_y >= state.columns:
            print("Move out of bounds!")
            return None

        target_cell = state.board[target_x][target_y]
        if target_cell.type not in ['Space', 'White']:
            print("Not Allowed Cell To Move!")
            return None
        current_coords = state.getMagnetCoords(magnet_type)
        if current_coords is None:
            return None

        current_x, current_y = current_coords
        new_state = deepcopy(state)
        # Move
        if target_cell.type == 'Space':
            new_state.board[target_x][target_y].type = magnet_type
        elif target_cell.type == 'White':
            new_state.board[target_x][target_y].type = f'White{magnet_type}'
        # Update the original
        if new_state.board[current_x][current_y].type == f'White{magnet_type}':
            new_state.board[current_x][current_y].type = 'White'
        else:
            new_state.board[current_x][current_y].type = 'Space'

        # Push or Pull if Possible
        self.checkRepelOrAttract(new_state, magnet_type, target_x, target_y)
        print(f"Moved {magnet_type} to ({target_x}, {target_y})")
        return new_state

    def getUserMove(self, state):
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
        new_state = self.checkMove(state, magnet_type, target_x, target_y)
        if not new_state:
            print("Move failed. Please try again.")
        else:
            self.current_state = new_state
            print("Move successful!")
            print(self.current_state)
            if self.checkSuccess(new_state):
                return True
            return False

    def checkRepelOrAttract(self, state, magnet_type, new_x, new_y):
        if magnet_type in ["Purple", 'WhitePurple']:
            self.repelMagnet(state, new_x, new_y)
        elif magnet_type in ["Red", 'WhiteRed']:
            self.attractMagnet(state, new_x, new_y)
        # print(self.initial_state)

    def repelMagnet(self, state, x, y):
        for j in range(state.columns):  # row
            if j != y:
                self.repelCell(state, x, j)
        for i in range(state.rows):  # column
            if i != x:
                self.repelCell(state, i, y)

    def repelCell(self, state, x, y):
        cell = state.board[x][y]
        if cell.type in ['Iron', 'Red', 'WhiteIron', 'WhiteRed', 'WhitePurple']:
            if cell.type == 'Iron':
                if self.isAdjacentToWhite(state, x, y):
                    cell.type = 'Space'
                    adjacent_white_cell = self.getAdjacentWhiteCell(
                        state, x, y)
                    if adjacent_white_cell:
                        adjacent_white_cell.type = 'WhiteIron'
                    print(
                        f"Cell at ({x}, {y}) repelled and merged into WhiteIron.")
                # else:
                #     cell.type = 'Space'
                #     adjacent_white_cell.type == 'Iron'

            elif cell.type == 'Red':
                if self.isAdjacentToWhite(state, x, y):
                    cell.type = 'Space'
                    adjacent_white_cell = self.getAdjacentWhiteCell(
                        state, x, y)
                    if adjacent_white_cell:
                        adjacent_white_cell.type = 'WhiteRed'
                    print(
                        f"Cell at ({x}, {y}) repelled and merged into WhiteRed.")
                # else:
                #     cell.type = 'Space'  # No merge, just clear the cell

    def attractMagnet(self, state, x, y):
        for j in range(state.columns):
            if j != y:
                self.pullCell(state, x, j, x, y)
        for i in range(state.rows):
            if i != x:
                self.pullCell(state, i, y, x, y)

    def pullCell(self, state, target_x, target_y, magnet_x, magnet_y):
        # target cell to check
        cell = state.board[target_x][target_y]
        if cell.type in ['Iron', 'Purple', 'WhiteIron', 'WhitePurple']:
            # Check vertical U-D
            if target_x < magnet_x:
                if target_x + 1 < state.rows:  # down
                    next_cell = state.board[target_x + 1][target_y]
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
                    next_cell = state.board[target_x - 1][target_y]
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
                if target_y + 1 < state.columns:  # R
                    next_cell = state.board[target_x][target_y + 1]
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
                    next_cell = state.board[target_x][target_y - 1]
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

    def isAdjacentToWhite(self, state, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < state.rows and 0 <= ny < state.columns:
                adjacent_cell = state.board[nx][ny]
                if adjacent_cell.type == 'White':
                    return True
        return False

    def getAdjacentWhiteCell(self, state, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < state.rows and 0 <= ny < state.columns:
                adjacent_cell = state.board[nx][ny]
                if adjacent_cell.type == 'White':
                    return adjacent_cell
        return None

    def getNeighbourCell(self, state, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < state.rows and 0 <= ny < state.columns:
                neighbour = state.board[nx][ny]
                return neighbour
        return None

    #!......................................................................................................⚡
    def bfs_solver(self):
        queue = deque([(self.initial_state, [])])  # state , path FIFO
        visited = set()
        while queue:
            current_state, path = queue.popleft()  # remove front
            if self.checkSuccess(current_state):
                print("bfs found success solution")
                return path
            if current_state in visited:
                continue
            visited.add(current_state)
            for magnet_type in ['Red', 'Purple', 'WhiteRed', 'WhitePurple']:
                cur_coords = current_state.getMagnetCoords(magnet_type)
                if cur_coords is None:
                    continue
                for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:

                    target_x, target_y = cur_coords[0]+ix, cur_coords[1]+iy
                    new_state = self.checkMove(
                        current_state, magnet_type, target_x, target_y)
                    if new_state and self.state_str(new_state) not in visited:
                        new_path = path + [{'magnet': magnet_type, 'x': target_x, 'y': target_y}]
                        queue.append((new_state, new_path))  # add to end

        print("bfs No solution found.")
        return None
    #!......................................................................................................⚡

    def dfs_solver(self):
        stack = [(self.initial_state, [])]  # state, path LIFO
        visited = set()

        while stack:
            current_state, path = stack.pop()
            state_here = self.state_str(current_state)
            if state_here in visited:
                continue
            visited.add(state_here)

            if self.checkSuccess(current_state):
                print("dfs Found success solution")
                return path

            for magnet_type in ['Red', 'Purple', 'WhiteRed', 'WhitePurple']:
                cur_coords = current_state.getMagnetCoords(magnet_type)
                if cur_coords is None:
                    continue

                for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    target_x, target_y = cur_coords[0] + ix, cur_coords[1] + iy
                    new_state = self.checkMove(
                        current_state, magnet_type, target_x, target_y)
                    # valid & not repetitive
                    if new_state and self.state_str(new_state) not in visited:
                        new_path = path +    [{'magnet': magnet_type, 'x': target_x, 'y': target_y}]
                        stack.append((new_state, new_path))

        print("dfs No solution found.")
        return None

    def state_str(self, state):
        return ''.join([''.join([cell.type for cell in row]) for row in state.board])

    def play(self, state):
        while True:
            self.getUserMove(state)
            if self.checkSuccess(self.current_state):
                print("WINNNNNNNNNNNN!!")
                break

    def bfs_play(self):
        solution_path = self.bfs_solver()
        if solution_path:
            print("Path to solution:")
            for move in solution_path:
                print(move)
        else:
            print("bfs Could not solve the puzzle.")

    def dfs_play(self):
        solution_path = self.dfs_solver()
        if solution_path:
            print("Path to solution:")
            for move in solution_path:
                print(move)
        else:
            print("dfs Could not solve the puzzle.")
