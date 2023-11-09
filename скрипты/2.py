# Напишите программу, которая принимает на вход(из файла либо из консоли)
# скобочную последовательность, а результатом работы которой является ответ,
# является ли данная скобочная последовательность правильной.
# Пример: “(()())()” - Правильная последовательность
# “(()))” - Неправильная последовательность
# “)())(” - Неправильная последовательность

def is_valid_bracket_sequence(sequence: str) -> bool:
    """Проверяет правильность скобочной последовательности."""
    balance = 0

    for bracket in sequence:
        if bracket == '(':
            balance += 1
        elif bracket == ')':
            balance -= 1
            if balance < 0:
                return False
        else:
            return False

    return balance == 0


def main():
    sequence = input("Введите скобочную последовательность: ")
    if is_valid_bracket_sequence(sequence):
        print("Правильная последовательность")
    else:
        print("Неверная последовательность")


if __name__ == "__main__":
    main()
