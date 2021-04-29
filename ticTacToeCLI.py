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

    def print(self):
        output_string = ""
        for choice in range(0, len(self.choices)):
            output_string += "|" + self.choices[choice]
            if (choice + 1) % 3 == 0:
                output_string += "|\n"
        print(output_string)


class Player:
    def __init__(self, sign):
        self.points = 0
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
    player1 = Player("X")
    player2 = Player("O")
    player1.add_sign(matchfield.choices, 1)
    player1.add_sign(matchfield.choices, 2)
    matchfield.print()

    for k, pattern_list in WINNER_PATTERNS.items():
        print(pattern_list)
    

if __name__ == '__main__':
    main()