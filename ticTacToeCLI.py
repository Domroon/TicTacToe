def print_matchfield(choices):
    output_string = ""
    for choice in range(0, len(choices)):
        output_string += "|" + choices[choice]
        if (choice + 1) % 3 == 0:
            output_string += "|\n" 
    print(output_string)

def main():
    choices = ["-","-","-","-","-","-","-","-","-"]
    print_matchfield(choices)
    


if __name__ == '__main__':
    main()