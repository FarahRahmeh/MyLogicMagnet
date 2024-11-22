
class Level:
    def __init__(self, level_grid, allowed_moves):
        self.level_grid = level_grid
        self.allowed_moves = allowed_moves

    def __str__(self):
        board_display = "\n".join(" ".join(row) for row in self.level_grid)
        # return f"Board:\n{board_display}\nAllowed Moves: {self.allowed_moves}\n"
        return f"{board_display}\n"
