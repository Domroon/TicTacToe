def print_matchfield(choices_list):
    output_string = ""
    for choice in range(0, len(choices_list)):
        output_string += "|" + choices_list[choice]
        if (choice + 1) % 3 == 0:
            output_string += "|\n" 
    print(output_string)


def get_choices_list(player_1_choices, player_2_choices):
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
    player_1_choices = [True] + [True] + [False for x in range(0, 7)]
    player_2_choices = [False for x in range(0, 9)]
    player_2_choices[4] = True
    player_2_choices[6] = True
    print_matchfield(get_choices_list(player_1_choices,player_2_choices))
    

if __name__ == '__main__':
    main()