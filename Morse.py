
morseNumbers = {'0': '-----',
                '1': '.----',
                '2': '..---',
                '3': '...--',
                '4': '....--',
                '5': '.....',
                '6': '-....',
                '7': '--...',
                '8': '---..',
                '9': '----.'}

    



def convert_num_to_morse(numbers):
    numbers = str(numbers)
    result = []

    for number in numbers:
        result+=[morseNumbers[number]]
        
    return result
