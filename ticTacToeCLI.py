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
        x_pattern = self._convert_pattern("X")
        o_pattern = self._convert_pattern("O")

        for key, pattern_list in WINNER_PATTERNS.items():
            if pattern_list == x_pattern:
                return "X"
            elif pattern_list == o_pattern:
                return "O"


    def print(self):
        output_string = ""
        for choice in range(0, len(self.choices)):
            output_string += "|" + self.choices[choice]
            if (choice + 1) % 3 == 0:
                output_string += "|\n"
        print(output_string)


class Player:
    def __init__(self, sign):
        self.sign = sign

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
    matchfield = Matchfield()
    while True:
        try:
            player_1 = Player(input("Player 1, please choose a sign (X or O): "))
            break
        except ValueError:
            print("Wrong Input. Please try again.")

    if player_1.sign == "X":
        player_2 = Player("O")
    else:
        player_2 = Player("X")

    print("Player 1 sign: ", player_1.sign)
    print("Player 2 sign: ", player_2.sign)

    matchfield.print()
    while True: 
        while True:
            try:
                player_1_pos = int(input("Player 1, please name a number (0-8): "))
                player_1.add_sign(matchfield.choices, player_1_pos)
                matchfield.print()
                break
            except ValueError:
                print("Please name a number!")
            except IndexError:
                print("Please name a number betwenn 0-8")

        if matchfield.determine_winner() == "X":
            print("Player with sign 'X' win!")
            break
        elif matchfield.determine_winner() == "O":
            print("Player with sign 'O' win!")
            break

        while True:
            try:    
                player_2_pos = int(input("Player 2, please name a number (0-8): "))
                player_2.add_sign(matchfield.choices, player_2_pos)
                matchfield.print()
                break
            except ValueError:
                print("Please name a number!")
            except IndexError:
                print("Please name a number betwenn 0-8")

        if matchfield.determine_winner() == "X":
            print("Player with sign 'X' win!")
            break
        elif matchfield.determine_winner() == "O":
            print("Player with sign 'O' win!")
            break


if __name__ == '__main__':
    main()