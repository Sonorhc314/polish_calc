import re
#import docstring

#This is your SRPN file. Make your changes here.

#globals----------------------------------------------------------------------
stack = []

#operand "r" prints random numbers using
#function in C rand() with the seed 1
#SRPN calculator prints 2 times the first 22 numbers
#since it is unlikely that we will need more than 44 random digits
#we can just loop through the array of 22 elements
pseudo_random = [
    1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335,
    719885386, 1649760492, 596516649, 1189641421, 1025202362, 1350490027,
    783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426,
    304089172, 1303455736, 35005211, 521595368
]
pseudo_random_index = -1

comment_open = False  #checks if a comment is open or closed

operations = {  #dictionary of operands that need 2 arguments
    '+': (lambda num1, num2: num1 + num2),
    '-': (lambda num1, num2: num1 - num2),
    '*': (lambda num1, num2: num1 * num2),
    '%': (lambda num1, num2: num1 % num2),
    '/': (lambda num1, num2: num1 / num2
          if (num2 != 0) else dev_power(num1, num2, 1)),
    '^': (lambda num1, num2: num1**num2
          if (num2 >= 0) else dev_power(num1, num2, 0))
}

operations2 = {  #dictionary of operands that don't need arguments
    'd': (lambda: display()),
    '=': (lambda: equal_display()),
    'r': (lambda: [check_stack_append(pseudo_random[pseudo_random_incr()])])
}

#globals----------------------------------------------------------------------


def equal_display():  #function for "=" operand
    if len(stack) > 0:
        res = stack.pop()
        print(int(res))
        saturation_check_append(res)
    else:
        print("Stack empty.")


def pseudo_random_incr():  #function to increment index that
    global pseudo_random_index  #goes through the array of pseudo random numbers
    if pseudo_random_index < len(pseudo_random) - 1:
        pseudo_random_index += 1
    else:  #loop array
        pseudo_random_index = 0
    return pseudo_random_index


def display():  #function for "d" operand
    if len(stack) > 0:  #if there are elements in the stack, print all of them
        for element in stack:
            print(int(element))
    else:
        print("-2147483648")  #if no elements, return minimum value


def dev_power(num1, num2, dev):  #depending on variable dev define function
    #(either for devision or power exception)
    if dev == 1:  #if 1 then the function if for division
        print("Divide by 0.")
    else:  #if not 1 then the function is for power
        print("Negative power.")
    saturation_check_append(num1)
    return num2


def check_stack_append(
        element):  #checks whether stack has enough space, appends element
    if len(stack) < 23:
        saturation_check_append(element)
    else:
        print("Stack overflow.")


def saturation_check_append(digit):  #check that we are working with numbers
    #that are within [-2147483647,...,2147483647] range
    if -2147483648 < digit < 2147483647:
        stack.append(digit)
    elif digit >= 2147483647:
        stack.append(2147483647)
    elif digit <= -2147483648:
        stack.append(-2147483648)


def calculate(
        operation):  #function to calculate operations that use 2 elements
    if operation in operations:
        if len(stack) > 1:
            num2 = stack.pop()
            num1 = stack.pop()
            res = operations[operation](num1, num2)
            saturation_check_append(float(res))
        else:
            print("Stack underflow.")


def display_equal(operation):  #display functions for "=" and "d"
    if operation in operations2:
        operations2[operation]()  #implement functions for the operand-key


def command_seperator(command):  #converts input into the list,
    #separetes elements of strings and digits

    command = re.split('(\d+)', command)
    blank_el = command.count('')
    for _ in range(blank_el):
        command.remove('')

    for minus in range(len(command) - 1):
        for character in command[minus]:
            if command[minus][-1] == '-':
                try:
                    int(command[minus + 1])
                    command[minus + 1] = '-' + command[minus + 1]
                    command.remove('-')
                except:
                    pass

    return command


def character_operations(el, character):  #function that determines
    #operation for el[character]
    global comment_open
    if el[character] in operations2:  # checks if element if "=" or "d"
        display_equal(el[character]
                      )  #if el is either d or equal we will get printed output
    elif el[character] in operations:  #checks if element is operand 
        #from operations dict
        calculate(el[character])
    elif el[character] == '#':
        if character < len(el) - 1:
            if el[character + 1] == ' ':
                comment_open = True
        else:
            comment_open = True
    else:
        if el[character] != ' ':
            print('Unrecognised operator', end=' ')
            print(f'or operand "{el[character]}"')


def process_command(command):
    global comment_open
    command = command_seperator(command)
    for el in command:
        if el.lstrip("-").isdigit():
            if comment_open is False:
                check_stack_append(float(el))
        else:
            for character in range(len(el)):
                if comment_open is False:
                    character_operations(el, character)
                else:
                    if el[character] == '#':
                        if el[character - 1] == ' ' or character == 0:
                            if len(el) == character + 1:
                                comment_open = False
                            elif el[character + 1] == ' ':
                                comment_open = False


#This is the entry point for the program.
#It is suggested that you do not edit the below,
#to ensure your code runs with the marking script
if __name__ == "__main__":
    while True:
        try:
            cmd = input()
            pc = process_command(cmd)
        except EOFError:
            exit()
