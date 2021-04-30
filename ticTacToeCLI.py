WINNER_PATTERNS = {
    1 : [1, 0, 0,
         0, 1, 0,
         0, 0, 1],

    2 : [0, 0, 1,
         0, 1, 0,
         1, 0, 0],

    3 : [1, 1, 1,
         0, 0, 0,
         0, 0, 0],

    4 : [0, 0, 0,
         1, 1, 1,
         0, 0, 0],

    5 : [0, 0, 0,
         0, 0, 0,
         1, 1, 1],

    6 : [1, 0, 0,
         1, 0, 0,
         1, 0, 0],

    7 : [0, 1, 0,
         0, 1, 0,
         0, 1, 0],

    8 : [0, 0, 1,
         0, 0, 1,
         0, 0, 1]
}


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
                player_pos = int(input(f'{player.name}, please name a number (0-8): '))
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


    def _convert_pattern(self, sign):
        num_pattern = []
        for pos in range(0, len(self.choices)):
            if self.choices[pos] == sign:
                num_pattern += [1]
            elif pos != len(self.choices):
                num_pattern += [0]

        return num_pattern
    

    def determine_winner(self):
        pass
        #if self.choices[0] == self.choices[1] == self.choices[2]:
        #    return self.choices[0]


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

    @property
    def sign(self):
        return self._sign

    @sign.setter
    def sign(self, sign):
        if not sign in ["X", "O"]:
            raise ValueError("Attribute must be 'X' or 'O'")
        self._sign = sign 

    def add_sign(self, choices, position):
        if choices[position] not in "-":
            raise ValueError("Position ist not empty")
        choices[position] = self.sign


def main():
    while True:
        try:
            game = Game()
            break
        except ValueError:
            print("Wrong Input. Please try again.")

    print(f'{game.player_1.name} sign: {game.player_1.sign}')
    print(f'{game.player_2.name} sign: {game.player_2.sign}\n')
    game.matchfield.print()

    while not game.get_winner():
        game.make_move(game.player_1)
        if game.get_winner():
            break
        game.make_move(game.player_2)


if __name__ == '__main__':
    main()