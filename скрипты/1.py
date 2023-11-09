# Напишите программу, которая запрашивает у пользователя число n,
# а затем выводит n первых строк треугольника Паскаля. Обеспечьте
# отказоустойчивость при введении пользователем не валидного значения
# n (т.е. не целого положительного числа)

def compute_next_row(previous_row):
    """Вычисляет следующую строку на основе предыдущей строки."""
    new_row = [1]
    for j in range(1, len(previous_row)):
        new_row.append(previous_row[j - 1] + previous_row[j])
    new_row.append(1)
    return new_row


def create_pascals_triangle(num_rows):
    """Генерирует треугольник Паскаля с заданным количеством строк."""
    if num_rows == 0:
        return []
    
    triangle = [[1]]
    for i in range(1, num_rows):
        triangle.append(compute_next_row(triangle[i - 1]))
    return triangle


def display_centered_row(row, max_width):
    """Печатает строку, центрированную по заданной максимальной ширине."""
    print(" ".join(map(str, row)).center(max_width))


def display_pascals_triangle(triangle):
    """Отображает треугольник Паскаля, центрируя каждую строку."""
    if not triangle:
        return

    max_width = len(" ".join(map(str, triangle[-1])))
    for row in triangle:
        display_centered_row(row, max_width)


def main():
    n = 0
    while n <= 0: 
        try: 
            n = int(input("Введите число строк треугольника Паскаля: "))
            if n <= 0:
                print("Пожалуйста, введите положительное число.")
            else:
                triangle = create_pascals_triangle(n)
                print("\nТреугольник Паскаля из первых", n, "строк:")
                display_pascals_triangle(triangle)
        except ValueError:
            print("Некорректный ввод. Пожалуйста, введите целое число.")


if __name__ == "__main__":
    main()

