def calculator(s):
    word_to_digit = {
        'ONE': '1',
        'TWO': '2',
        'THR': '3',
        'FOU': '4',
        'FIV': '5',
        'SIX': '6',
        'SEV': '7',
        'EIG': '8',
        'NIN': '9',
        'ZER': '0'
    }

    digit_to_word = {v: k for k, v in word_to_digit.items()}

    expr = s
    for w, d in word_to_digit.items():
        expr = expr.replace(w, d)

    result = str(eval(expr))

    for d, w in digit_to_word.items():
        result = result.replace(d, w)

    return result


n = input()
print(calculator(n))