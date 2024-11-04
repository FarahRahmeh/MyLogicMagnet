class Cell:
    def __init__(self, x, y, type) -> None:
        self.x = x
        self.y = y
        self.type = type

    def __str__(self) -> str:
        if self.type == 'Out':
            return '🔳'
        elif self.type == 'Space':
            return '⚫'
        elif self.type == 'Iron':
            return '🔵'
        elif self.type == 'White':
            return '⚪'
        elif self.type == 'Red':
            return '🔴'
        elif self.type == 'Purple':
            return '🟣'
        elif self.type == 'WhiteIron':
            return '🔘'
        elif self.type == 'WhiteRed':
            return '🟥'
        elif self.type == 'WhitePurple':
            return '🟪'
        # return '⚫'

