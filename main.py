import random
import math

class TicTacToe:

    def __init__(self):
        self.field = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.list_players = ['user', 'easy', 'medium', 'hard']

    def print_field(self):
        return print(
            f"""\
            ---------
            | {self.field[0][0]} {self.field[1][0]} {self.field[2][0]} |
            | {self.field[0][1]} {self.field[1][1]} {self.field[2][1]} |
            | {self.field[0][2]} {self.field[1][2]} {self.field[2][2]} |
            ---------\
            """
        )

    def game_setup(self):
        input_ = input('input: ')
        # input_ = 'start user hard'
        input_values = input_.split()

        while True:
            if input_values[0] == 'exit':
                break
            elif input_values[0] == 'start' and input_values[1] in self.list_players and input_values[
                2] in self.list_players:
                player1 = Player(self.field, 'X', input_values[1])
                player2 = Player(self.field, 'O', input_values[2])
                return player1, player2
            else:
                print('Bad parameters')

    def game_flow(self):
        player1, player2 = self.game_setup()
        self.print_field()
        while True:

            player1.make_move()
            self.print_field()
            result = game_state(self.field)
            if result:
                print(result)
                exit()

            player2.make_move()
            self.print_field()
            result = game_state(self.field)
            if result:
                print(result)
                exit()


def game_state(field):
    field_str = field[0] + field[1] + field[2]
    global rules
    rules = [
        # Vertical
        field[0], field[1], field[2],
        # Horizontal
        field_str[::3], field_str[1::3], field_str[2::3],
        # Diagonal
        field_str[::4], field_str[2:7:2]
    ]

    for rule in rules:
        if rule.count('X') == 3:
            return 'X wins'
        elif rule.count('O') == 3:
            return 'O wins'
        elif ' ' not in field_str:
            return 'Draw'


class Player:

    def __init__(self, field, item, level):
        self.field = field
        self.item = item
        self.level = level

    def get_coords(self):
        while True:
            column, row = input('Enter the coordinates: ').split()
            if not column.isnumeric() or not row.isnumeric():
                print('You should enter numbers!')
            elif (int(column) > 3) or (int(row) > 3):
                print('Coordinates should be from 1 to 3!')
            elif self.field[int(column) - 1][abs(int(row) - 3)] != ' ':
                print('This cell is occupied! Choose another one!')
            else:
                self.field[int(column) - 1][abs(int(row) - 3)] = self.item
                break

    def easy_level(self):
        print('Making move level "easy"')

        while True:
            column, row = random.randint(0, 2), random.randint(0, 2)
            if self.field[column][row] == ' ':
                self.field[column][row] = self.item
                break

    def analyze(self, item1):
        # Vertical
        for ix, column in enumerate(self.field):
            if column.count(item1) == 2 and ' ' in column:
                row = [x for x in range(len(column)) if column[x] == ' ']
                return ix, row[0]

        # Horizontal
        for i in range(3):
            h_list = []
            for col in self.field:
                h_list.append(col[i])
            if h_list.count(item1) == 2 and ' ' in h_list:
                row = [x for x in range(len(h_list)) if h_list[x] == ' ']
                return row[0], i

        # Diagonal
        rows = [self.field[0][0] + self.field[1][1] + self.field[2][2],
                self.field[0][2] + self.field[1][1] + self.field[2][0]
                ]

        indexes = [[[0, 0], [1, 1], [2, 2]],
                   [[0, 2], [1, 1], [2, 0]]]

        for ix, column in enumerate(rows):
            if column.count(item1) == 2 and ' ' in column:
                row = [x for x in range(len(column)) if column[x] == ' ']
                return indexes[ix][row[0]]

    def medium_level(self):
        print('Making move level "medium"')
        items = ['X', 'O']
        items.remove(self.item)
        opponent = items[0]

        try:
            column, row = self.analyze(item1=self.item)
        except TypeError:
            try:
                column, row = self.analyze(item1=opponent)
            except TypeError:
                while True:
                    column, row = random.randint(0, 2), random.randint(0, 2)
                    if self.field[column][row] == ' ':
                        return column, row

        return column, row

    def hard_level(self):
        print('Making move level "hard"')

        best_score = -math.inf
        column = None
        row = None

        for ix, col in enumerate(self.field):
            for i in range(len(col)):
                if self.field[ix][i] == ' ':
                    self.field[ix][i] = self.item
                    score = self.minimax(board=self.field, is_maximizing=False)
                    self.field[ix][i] = ' '
                    if score > best_score:
                        best_score = score
                        column = ix
                        row = i

        return [column, row]

    def minimax(self, board, is_maximizing):
        if self.item == 'O':
            scores = {
            'X wins': -1,
            'O wins': 1,
            'Draw': 0
            }
        else:
            scores = {
                'X wins': 1,
                'O wins': -1,
                'Draw': 0
            }

        items = ['X', 'O']
        items.remove(self.item)
        opponent = items[0]

        result = game_state(board)
        if result:
            return scores[result]

        if is_maximizing:
            best_score = -math.inf
            for ix, col in enumerate(board):
                for i in range(len(col)):
                    if board[ix][i] == ' ':
                        board[ix][i] = self.item
                        score = self.minimax(board, False)
                        board[ix][i] = ' '
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for ix, col in enumerate(board):
                for i in range(len(col)):
                    if board[ix][i] == ' ':
                        board[ix][i] = opponent
                        score = self.minimax(board, True)
                        board[ix][i] = ' '
                        best_score = min(score, best_score)
            return best_score

    def make_move(self):

        if self.level == 'user':
            self.get_coords()
        elif self.level == 'easy':
            self.easy_level()
        elif self.level == 'medium':
            column, row = self.medium_level()
            self.field[column][row] = self.item
        else:
            column, row = self.hard_level()
            self.field[column][row] = self.item


game = TicTacToe().game_flow()
