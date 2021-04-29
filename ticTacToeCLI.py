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
            raise ValueError
        self._sign = sign 

    def add_sign(self, choices, position):
        choices[position] = self.sign

    
def print_matchfield(choices_list):
    output_string = ""
    for choice in range(0, len(choices_list)):
        output_string += "|" + choices_list[choice]
        if (choice + 1) % 3 == 0:
            output_string += "|\n" 
    print(output_string)


def make_choices_list(player_1_choices, player_2_choices):
    choices_list = ""
    for choice in range(0, len(player_1_choices)):
        if player_1_choices[choice] == False and player_2_choices[choice] == False:
            choices_list += "-"
        elif player_1_choices[choice] == True:
            choices_list += "X"
        elif player_2_choices[choice] == True:
            choices_list += "O"
        else:
            raise ValueError

    return choices_list


def verify_choice(choice, player_1_choices, player_2_choices):
    choice = int(choice)
    if not 0 <= choice <= len(player_1_choices):
        return False
    elif player_1_choices[choice] == True and player_2_choices[choice] == True:
        return False
    else:
        return True


def main():
    matchfield = Matchfield()
    player1 = Player("X")
    player2 = Player("O")
    player1.add_sign(matchfield.choices, 1)
    player2.add_sign(matchfield.choices, 4)
    matchfield.print()
    

if __name__ == '__main__':
    main()