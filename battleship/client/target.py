class Target:
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col

    def getCoordinates(self):
        return (self.row, self.col)

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col
