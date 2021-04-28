class Player:
    def __init__(self):
        self.choices = [False for choice in range(0,9)]


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


def main():
    player1 = Player()
    player2 = Player()

    choices_list = make_choices_list(player1.choices, player2.choices)

    print_matchfield(choices_list)
    

if __name__ == '__main__':
    main()