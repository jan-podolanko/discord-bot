class TicTacToe:
    def __init__(self):
        self.board = []

    def create_board(self):
        return
    def check_if_filled(self):
        for row in self.board:
            for item in row:
                if item == ' ':
                    return False
            return True

    def check_if_won(self):
        #check columns
        for row in self.board:
            for item in row:
                if item == ' ':
                    return False
            return True