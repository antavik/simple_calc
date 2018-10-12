import operator
from collections import namedtuple


OPER = namedtuple('operator', 'priority func string')
NUMBERS = '1234567890'
OPERANDS = {
    '+': OPER(1, operator.add, '+'),
    '-': OPER(1, operator.sub, '-'),
    '*': OPER(2, operator.mul, '*'),
    '/': OPER(2, operator.truediv, '/'),
    '^': OPER(3, operator.pow, '^'),
}


def calc():
    raw_string = input("Input your expression: ")

    expression = clean_string(raw_string)
    polish_notation = prepare_polish_string(expression)
    print(polish_notation)
    result = read_polish_string(polish_notation)
    print(result)


def clean_string(raw_string):
    return raw_string.replace(" ", "")


def prepare_polish_string(expression):
    operation_stack = []
    output_expression = []

    string_length = len(expression)
    number = ''

    def convert_string(number):
        if number:
            new_number = float(number) if '.' in number else int(number)
            output_expression.append(new_number)

    for i, s in enumerate(expression):
        if s in NUMBERS or s == '.':
            number += s
        else:
            convert_string(number)
            number = ''

            operand = OPERANDS.get(s)
            if operand:
                if operation_stack and operation_stack[-1].priority >= operand.priority:
                    output_expression.append(operation_stack.pop())
                operation_stack.append(operand)
            else:
                raise TypeError('Symbol - "{}" is not supported'.format(s))

    convert_string(number)

    for i in operation_stack[::-1]:
        output_expression.append(i)

    return output_expression


def read_polish_string(pol_string):
    stack = []

    for el in pol_string:
        if isinstance(el, int) or isinstance(el, float):
            stack.append(el)
        else:
            b, a = stack.pop(), stack.pop()
            stack.append(el.func(a, b))

    return stack[0]


if __name__ == '__main__':
    calc()
