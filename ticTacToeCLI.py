

class Matchfield:
    def __init__(self):
        self.choices = ['-', '-', '-', '-', '-', '-', '-', '-', '-']

    def determine_winner(self):
        if self.choices[0] == self.choices[1] == self.choices[2]:
            return self.choices[0]
        elif self.choices[3] == self.choices[4] == self.choices[5]:
            return self.choices[3]
        elif self.choices[6] == self.choices[7] == self.choices[8]:
            return self.choices[6]
        elif self.choices[0] == self.choices[3] == self.choices[6]:
            return self.choices[0]
        elif self.choices[1] == self.choices[4] == self.choices[7]:
            return self.choices[1]
        elif self.choices[2] == self.choices[5] == self.choices[8]:
            return self.choices[2]
        elif self.choices[0] == self.choices[4] == self.choices[8]:
            return self.choices[0]
        elif self.choices[2] == self.choices[4] == self.choices[6]:
            return self.choices[2]  
        else:
            counter = 0
            for sign in self.choices:
                if sign != "-":
                    counter += 1
                    if counter == 9:
                        return "Nobody"

    def print(self):
        output_string = ""
        for choice in range(0, len(self.choices)):
            output_string += "|" + self.choices[choice]
            if (choice + 1) % 3 == 0:
                output_string += "|\n"
        print(output_string)


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
                print("Please name a number betwenn 0-8")


def main():
    pass


if __name__ == '__main__':
    main()