class State:
    def __init__(self, rows, columns, board) -> None:
        self.rows = rows
        self.columns = columns
        self.board = board

    def __str__(self) -> None:
        # Column headers
        grid = "     " + " ".join(f"{j:2}" for j in range(self.columns)) + "\n"
        grid += "    " + "---" * self.columns + "\n"  # Separator line

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
