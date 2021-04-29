class Matchfield:
    def __init__(self, choices):
        self.choices = choices

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, choices):
        self._choices = choices


class Player:
    def __init__(self):
        self.points = 0

    
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
    matchfield = Matchfield(["-" for choice in range(0, 9)])
    print(matchfield.choices)
    matchfield.choices = ["X" for choice in range(0, 9)]
    print(matchfield.choices)
    matchfield.choices[0] = "O"
    matchfield.choices[3] = "O"
    print(matchfield.choices)
    

if __name__ == '__main__':
    main()