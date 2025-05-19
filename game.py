from copy import deepcopy
from collections import deque
import heapq



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

    def checkMove(self, state, magnet_type, aim_x, aim_y):  # هل الحركة متاحة؟ هل تؤثر على شيء؟
        if aim_x < 0 or aim_x >= state.rows or aim_y < 0 or aim_y >= state.columns:
            print("Move out of bounds!")
            return None

        aim_cell = state.board[aim_x][aim_y]
        if aim_cell.type not in ['Space', 'White']:
            print("Not Allowed Cell To Move!")
            return None
        current_coords = state.getMagnetCoords(magnet_type)
        if current_coords is None:
            return None

        current_x, current_y = current_coords
        new_state = deepcopy(state)
        # Move to new
        if aim_cell.type == 'Space':
            new_state.board[aim_x][aim_y].type = magnet_type
        elif aim_cell.type == 'White':
            new_state.board[aim_x][aim_y].type = f'White{magnet_type}'
        # Update the prev
        if new_state.board[current_x][current_y].type == f'White{magnet_type}':
            new_state.board[current_x][current_y].type = 'White'
        else:
            new_state.board[current_x][current_y].type = 'Space'
        # Push or Pull
        self.checkRepelOrAttract(new_state, magnet_type, aim_x, aim_y)
        print(f"{magnet_type} moved to ({aim_x}, {aim_y})")
        return new_state

    def getUserMove(self, state):
        valid_magnets = ['Red', 'Purple', 'WhiteRed', 'WhitePurple']
        magnet_type = input(f"choose magnet type ({', '.join(valid_magnets)}): ").strip()
        if magnet_type not in valid_magnets:
            print("Invalid magnet type!")
            return False
        try:
            aim_x = int(input("Enter aim row: ").strip())
            aim_y = int(input("Enter aim column: ").strip())
        except ValueError:
            print("Invalid coordinates!")
            return False
        new_state = self.checkMove(state, magnet_type, aim_x, aim_y)
        if not new_state:
            print("Move failed try again")
        else:
            self.current_state = new_state
            print("Move successful")
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

    def repelMagnet(self, state, x, y):  # المغناطيس النهدي
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
                if self.isWhiteNear(state, x, y):
                    cell.type = 'Space'
                    adjacent_white_cell = self.getWhiteNear(state,x,y)
                    if adjacent_white_cell:
                        adjacent_white_cell.type = 'WhiteIron'
                    print(f"Cell at ({x}, {y}) repelled and merged into WhiteIron.")
                # else:
                #     cell.type = 'Space'
                #     adjacent_white_cell.type == 'Iron'

            elif cell.type == 'Red':
                if self.isWhiteNear(state, x, y):
                    cell.type = 'Space'
                    adjacent_white_cell = self.getWhiteNear(state, x, y)
                    if adjacent_white_cell:
                        adjacent_white_cell.type = 'WhiteRed'
                    print(f"Cell at ({x}, {y}) repelled and merged into WhiteRed.")
                # else:
                #     cell.type = 'Space'  # No merge, just clear the cell

    def attractMagnet(self, state, x, y):  # المغناطيس الأحمر
        for j in range(state.columns):
            if j != y:
                self.pullCell(state, x, j, x, y)
        for i in range(state.rows):
            if i != x:
                self.pullCell(state, i, y, x, y)

    def pullCell(self, state, aim_x, aim_y, magnet_x, magnet_y):  # ! red magnet
        # aim cell to check
        cell = state.board[aim_x][aim_y]
        if cell.type in ['Iron', 'Purple', 'WhiteIron', 'WhitePurple']:
            # Check vertical U-D
            if aim_x < magnet_x:
                if aim_x + 1 < state.rows:  # down
                    next_cell = state.board[aim_x + 1][aim_y]
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

            elif aim_x > magnet_x:
                # up
                if aim_x - 1 >= 0:
                    next_cell = state.board[aim_x - 1][aim_y]
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
            if aim_y < magnet_y:
                if aim_y + 1 < state.columns:  # R
                    next_cell = state.board[aim_x][aim_y + 1]
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
            elif aim_y > magnet_y:
                if aim_y - 1 >= 0:  # L
                    next_cell = state.board[aim_x][aim_y - 1]
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
                print(f"Cell at ({aim_x}, {aim_y}) cannot move closer to magnet.")

    def isWhiteNear(self, state, x, y):
        for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + ix, y + iy
            if 0 <= nx < state.rows and 0 <= ny < state.columns:
                adjacent_cell = state.board[nx][ny]
                if adjacent_cell.type == 'White':
                    return True
        return False

    def getWhiteNear(self, state, x, y):
        for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + ix, y + iy
            if 0 <= nx < state.rows and 0 <= ny < state.columns:
                adjacent_cell = state.board[nx][ny]
                if adjacent_cell.type == 'White':
                    return adjacent_cell
        return None

    def getNeighbourCell(self, state, x, y):
        for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + ix, y + iy
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
                    aim_x, aim_y = cur_coords[0]+ix, cur_coords[1]+iy
                    new_state = self.checkMove(
                        current_state, magnet_type, aim_x, aim_y)
                    if new_state and self.state_str(new_state) not in visited:
                        new_path = path +[f"'{magnet_type}' ({aim_x},{aim_y})"]
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
                    aim_x, aim_y = cur_coords[0] + ix, cur_coords[1] + iy
                    new_state = self.checkMove(
                        current_state, magnet_type, aim_x, aim_y)
                    # valid & not repetitive
                    if new_state and self.state_str(new_state) not in visited:
                        new_path = path +[f"'{magnet_type}' ({aim_x},{aim_y})"]
                        stack.append((new_state, new_path))

        print("dfs No solution found.")
        return None
#!......................................................................................................⚡

    def ucs_solver(self):
        pqueue = [(0, self.initial_state, [])]
        visited = set()

        while pqueue:
            cost, current_state, path = heapq.heappop(pqueue)
            print(f"Visiting State with Cost: {cost}")
            print(current_state)
            if self.checkSuccess(current_state):
                print("UCS found success solution")
                return path

            state_here = self.state_str(current_state)
            if state_here in visited:
                continue
            visited.add(state_here)
            for magnet_type in ['Red', 'Purple', 'WhiteRed', 'WhitePurple']:
                cur_coords = current_state.getMagnetCoords(magnet_type)
                if cur_coords is None:
                    continue
                for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    aim_x, aim_y = cur_coords[0] + ix, cur_coords[1] + iy
                    new_state = self.checkMove(
                        current_state, magnet_type, aim_x, aim_y)

                    if new_state and self.state_str(new_state) not in visited:
                        move_cost = self.calCost()
                        new_cost = cost+move_cost
                        new_path = path +[f"'{magnet_type}' ({aim_x},{aim_y})"]
                        heapq.heappush(pqueue, (new_cost, new_state, new_path))

        print("UCS No solution found.")
        return None
#!......................................................................................................⚡

    def heuristic(self, state):
        cnt = 0
        for row in state.board:
            for cell in row:
                if cell.type == 'White':
                    cnt += 1
        return cnt
#!......................................................................................................⚡

    def hill_climbing_solver(self):
        current_state = self.initial_state
        path = []
        visited = set()
        while True:
            if self.checkSuccess(current_state):
                print("Hill climbing found success solution")
                return path 
            state_here = self.state_str(current_state)
            if state_here in visited:
                print("Cycle found and No better solution found")
                return None
            visited.add(state_here)
            best_son_state = None
            best_son_heuristic = self.heuristic(current_state)
            for magnet_type in ['Red', 'Purple', 'WhiteRed', 'WhitePurple']:
                cur_coords = current_state.getMagnetCoords(magnet_type)
                if cur_coords is None:
                    continue
                for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    aim_x, aim_y = cur_coords[0] + ix, cur_coords[1] + iy
                    new_state = self.checkMove(current_state, magnet_type, aim_x, aim_y)
                    if new_state:
                        new_heuristic = self.heuristic(new_state)
                        if new_heuristic < best_son_heuristic:
                            best_son_heuristic = new_heuristic
                            best_son_state = new_state
                            best_son_step = f"'{magnet_type}' ({aim_x},{aim_y})"
            if best_son_state and best_son_heuristic < self.heuristic(current_state):
                current_state = best_son_state
                path.append(best_son_step)
            else:
                print("No better son found")
                return None

#!......................................................................................................⚡

    def a_star_solver(self):
        pqueue = [(0,0, self.initial_state, [])]
        visited = set()

        while pqueue:
            cost_heurstic,all_cost, current_state, path = heapq.heappop(pqueue)
            if self.checkSuccess(current_state):
                print("A* found a success solution")
                
                return path
            state_here = self.state_str(current_state)
            if state_here in visited:
                continue
            visited.add(state_here)
            for magnet_type in ['Red', 'Purple', 'WhiteRed', 'WhitePurple']:
                cur_coords = current_state.getMagnetCoords(magnet_type)
                if cur_coords is None:
                    continue
                for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    aim_x, aim_y = cur_coords[0] + ix, cur_coords[1] + iy
                    new_state = self.checkMove(
                        current_state, magnet_type, aim_x, aim_y)
                    if new_state and self.state_str(new_state) not in visited:
                        heu_cost = self.heuristic(new_state)
                        all_cost= all_cost + self.calCost()
                        cost_heurstic = all_cost + heu_cost
                        new_path = path +[f"'{magnet_type}' ({aim_x},{aim_y})"]
                        heapq.heappush(
                            pqueue, (cost_heurstic,all_cost, new_state, new_path))

        print("A* could not find a solution.")
        return None


#!......................................................................................................⚡

    def state_str(self, state):
        return ''.join([''.join([cell.type for cell in row]) for row in state.board])

    def play(self, state):
        while True:
            self.getUserMove(state)
            if self.checkSuccess(self.current_state):
                print("WINNNNNNNNNNNN!!")
                break

    def bfs_play(self):
        path_to_ans = self.bfs_solver()
        if path_to_ans:
            print("Path to solution:")
            for move in path_to_ans:
                print(move)
        else:
            print("bfs could not solve the game")

    def dfs_play(self):
        path_to_ans = self.dfs_solver()
        if path_to_ans:
            print("Path to solution:")
            for move in path_to_ans:
                print(move)
        else:
            print("dfs could not solve the game")

    def ucs_play(self):
        path_to_ans = self.ucs_solver()
        if path_to_ans:
            print("Path to solution:")
            for move in path_to_ans:
                print(move)
        else:
            print("UCS could not solve the game")

    def hill_climbing_play(self):
        path_to_ans = self.hill_climbing_solver()
        if path_to_ans:
            print("Path to solution:")
            for move in path_to_ans:
                print(move)
        else:
            print("Hill climbing could not solve the game")

    def a_star_play(self):
        path_to_ans = self.a_star_solver()
        if path_to_ans:
            print("Path to solution:")
            for move in path_to_ans:
                print(move)
        else:
            print("A* could not solve the game")

    def calCost(self):
        return 1
