WIN_INDICES = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], # horizontal
    [0, 3, 6], [1, 4, 7], [2, 5, 8], # vertical
    [0, 4, 8], [2, 4, 6]             # diagonal
]


class Game:
    def __init__(self):
        self.matchfield = Matchfield()
        self.player_1 = Player(input("Player 1, please choose a sign: "), "Player 1")
        self.player_2 = Player(self.get_sign(), "Player 2")

    def get_sign(self):
        if self.player_1.sign == "X":
            return "O"
        else:
            return "X"

    def make_move(self, player):
        while True:
            try:
                player_pos = int(input(f'{player.name}, please name a number (1-9): ')) - 1
                player.add_sign(self.matchfield.choices, player_pos)
                self.matchfield.print()
                break
            except ValueError:
                print("Wrong Input. Please try again.")
            except IndexError:
                print("Please name a number betwenn 0-8")
        
    def get_winner(self):
        if self.matchfield.determine_winner() == "X":
            print("Player with sign 'X' win!")
            return True
        elif self.matchfield.determine_winner() == "O":
            print("Player with sign 'O' win!")
            return True
        elif self.matchfield.determine_winner() == "Nobody":
            print("Nobody wins!")
            return True
        else:
            return False


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


def main():
    pass


if __name__ == '__main__':
    main()