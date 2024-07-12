def lcm(numbers):
    final_answer = 0
    for i in numbers:
        try:
            num = int(i)
        except ValueError:
            return "Error: Wrong data type inputted"
    lcm_found = False
    lcmGuess = 0
    while lcm_found == False:
        lcmGuess += 1
        lcm_found = True
        for i in numbers:
            i = int(i)
            if lcmGuess % i != 0:
                lcm_found = False
                break
    final_answer = lcmGuess

    return final_answer