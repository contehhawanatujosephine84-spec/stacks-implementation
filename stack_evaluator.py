class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise ValueError("Cannot pop from an empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise ValueError("Cannot peek an empty stack")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0


OPERATORS = {
    "+": (1, lambda left, right: left + right),
    "-": (1, lambda left, right: left - right),
    "*": (2, lambda left, right: left * right),
    "/": (2, lambda left, right: left / right),
}


def is_separator(line):
    stripped = line.strip()
    return stripped != "" and all(character == "-" for character in stripped)


def tokenize(expression):
    tokens = []
    index = 0
    previous_type = "operator"

    while index < len(expression):
        character = expression[index]

        if character.isspace():
            index += 1
            continue

        if character.isdigit() or character == "." or (
            character == "-"
            and previous_type in ("operator", "left_paren")
            and index + 1 < len(expression)
            and (expression[index + 1].isdigit() or expression[index + 1] == ".")
        ):
            start = index
            if expression[index] == "-":
                index += 1
            decimal_count = 0

            while index < len(expression) and (
                expression[index].isdigit() or expression[index] == "."
            ):
                if expression[index] == ".":
                    decimal_count += 1
                    if decimal_count > 1:
                        raise ValueError(f"Invalid number in expression: {expression}")
                index += 1

            tokens.append(float(expression[start:index]))
            previous_type = "number"
            continue

        if character in OPERATORS:
            tokens.append(character)
            previous_type = "operator"
            index += 1
            continue

        if character == "(":
            tokens.append(character)
            previous_type = "left_paren"
            index += 1
            continue

        if character == ")":
            tokens.append(character)
            previous_type = "right_paren"
            index += 1
            continue

        raise ValueError(f"Invalid character '{character}' in expression: {expression}")

    return tokens


def apply_operator(values, operators):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()

    if operator == "/" and right == 0:
        raise ZeroDivisionError("Division by zero is not allowed")

    values.push(OPERATORS[operator][1](left, right))


def evaluate_expression(expression):
    values = Stack()
    operators = Stack()

    for token in tokenize(expression):
        if isinstance(token, float):
            values.push(token)
        elif token == "(":
            operators.push(token)
        elif token == ")":
            while not operators.is_empty() and operators.peek() != "(":
                apply_operator(values, operators)
            if operators.is_empty():
                raise ValueError(f"Mismatched parentheses in expression: {expression}")
            operators.pop()
        else:
            while (
                not operators.is_empty()
                and operators.peek() != "("
                and OPERATORS[operators.peek()][0] >= OPERATORS[token][0]
            ):
                apply_operator(values, operators)
            operators.push(token)

    while not operators.is_empty():
        if operators.peek() == "(":
            raise ValueError(f"Mismatched parentheses in expression: {expression}")
        apply_operator(values, operators)

    result = values.pop()
    if not values.is_empty():
        raise ValueError(f"Invalid expression: {expression}")

    return result


def format_result(value):
    if value.is_integer():
        return str(int(value))
    return f"{value:.10f}".rstrip("0").rstrip(".")


def evaluate_file(input_file="input.txt", output_file="output.txt"):
    output_lines = []

    with open(input_file, "r", encoding="utf-8") as file:
        for raw_line in file:
            line = raw_line.rstrip("\n")

            if line.strip() == "":
                output_lines.append("")
            elif is_separator(line):
                output_lines.append(line)
            else:
                output_lines.append(format_result(evaluate_expression(line)))

    with open(output_file, "w", encoding="utf-8") as file:
        file.write("\n".join(output_lines))
        file.write("\n")


if __name__ == "__main__":
    evaluate_file()
