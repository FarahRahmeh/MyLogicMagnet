
class Level:
    def __init__(self, level_grid):
        self.level_grid = level_grid

    def __str__(self):
        board_display = "\n".join(" ".join(row) for row in self.level_grid)
        return f"{board_display}\n"
