from itertools import cycle

class Player:
    def __init__(self, sign, name):
        self.sign = sign
        self.name = name

    def __str__(self):
        return f"{self.name} Sign: {self.sign}"


class Game:
    SIGNS = ["X", "O"]
    WIN_INDICES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], # horizontal
    [0, 3, 6], [1, 4, 7], [2, 5, 8], # vertical
    [0, 4, 8], [2, 4, 6]             # diagonal
]
    def __init__(self):
        self.field = ['-'] * 9
        self.players = [
            Player(sign, f"Player {index}")
            for index, sign in enumerate(self.SIGNS, 1)
        ]

    def play(self):
        for player in self.players:
            print(player)
        print()
        self.print_field()
        for player in cycle(self.players):
            self.make_move(player)
            self.print_field()
            winner = self.determine_winner()
            if winner:
                break
        print(f"Winner is {winner}")

    def make_move(self, player):
        while True:
            try:
                player_pos = int(input(f'{player.name}, please name a number (1-9): ')) - 1
                self.add_sign(player, player_pos)
                break
            except ValueError:
                print("Wrong Input. Please try again.")
            except IndexError:
                print("Please name a number between 0-8")

    def determine_winner(self):
        for indices in self.WIN_INDICES:
            choices = set(self.field[i] for i in indices)
            if len(choices) == 1 and choices != {'-'}:
                return choices.pop()
        if not any(c=='-' for c in self.field):
            return 'Nobody'

    def print_field(self):
        for i in range (0, len(self.field), 3):
            print(f"|{'|'.join(self.field[i:i+3])}|")

    def add_sign(self, player, position):
        if self.field[position] != "-":
            raise ValueError("Position is not empty")
        self.field[position] = player.sign


def main():
    game = Game()
    game.play()


if __name__ == '__main__':
    main()