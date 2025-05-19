

class State:
    def __init__(self, rows, columns, board, cost,heurstic) -> None:
        self.rows = rows
        self.columns = columns
        self.board = board
        self.cost = cost
        self.heurstic = heurstic        

    def __str__(self) -> None:
        grid = f"Cost: {self.cost}\n"
        # Column headers
        grid = "     " + " ".join(f"{j:2}" for j in range(self.columns)) + "\n"
        grid += "    " + "---" * self.columns + "\n"  

        for i, row in enumerate(self.board):
            grid += f"{i:2} | "  # Row header with index
            for cell in row:
                grid += str(cell) + " "
            grid += "\n"
        return grid

    def getMagnetCoords(self, magnet_type):

        for row in self.board:
            for cell in row:
                if cell.type == magnet_type or cell.type == f'White{magnet_type}':
                    return cell.x, cell.y
        return None

    def __lt__(self, other):   # less than
        return self.cost < other.cost

    