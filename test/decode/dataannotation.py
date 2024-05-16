def decode(message_file):
    dictionary = {}
    number_of_lines = 0
    output = ''

    with open(f'{message_file}', 'r') as file:
        for line in file:
            line = line.strip('\n')
            pair = line.split(' ')
            dictionary[int(pair[0])] = pair[1]
            number_of_lines = number_of_lines + 1


    row = 1
    column = 1
    counter = 0

    while counter < number_of_lines:
        if column < row:
            column += 1
        else:
            output = output + dictionary[counter + 1] + ' '
            row += 1
            column = 1
        counter = counter + 1

    return output
    



def main():
    file = 'message_file.txt'
    print(decode(file))


main()