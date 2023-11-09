# Шифр Цезаря — это вид шифра подстановки, в котором каждый символ
# в открытом тексте заменяется символом, находящимся на некотором
# постоянном числе позиций левее или правее него в алфавите.
# Напишите программу, которая реализует шифрование Цезаря.
# Входные данные: путь до изначального файла с текстом,
# требуемый сдвиг и язык текста(на выбор английский либо русский).
# Результат работы - новый файл с зашифрованным текстом.

def input_filename() -> str:
    return input("Укажите путь к исходному файлу: ")


def input_language() -> str:
    return input("Выберите язык текста (английский или русский): ")


def get_cesar_input() -> tuple:
    filename = input_filename()
    offset = input_positive_integer("Укажите необходимый сдвиг: ")
    language = input_language()

    return filename, offset, language

def cesar_encrypt_string(text: str, offset: int, alphabet: str) -> str:
    result = ""
    size = len(alphabet)

    for char in text:
        if char.lower() in alphabet:
            idx = alphabet.index(char.lower())
            encrypted_char = alphabet[(idx + offset) % size]
            if char.isupper():
                encrypted_char = encrypted_char.upper()
            result += encrypted_char
        else:
            result += char

    return result

def input_positive_integer(prompt: str) -> int:
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            else:
                raise ValueError("Значение должно быть положительным числом.")
        except ValueError as e:
            print(e)

def cesar_encrypt_file(input_filename: str, offset: int, alphabet: str, output_filename: str = "out.txt"):
    try:
        with open(input_filename, "r", encoding="utf-8") as infile, \
             open(output_filename, "w", encoding="utf-8") as outfile:
            for line in infile:
                outfile.write(cesar_encrypt_string(line, offset, alphabet))
    except FileNotFoundError:
        print("Указан неверный путь к файлу.")
    except OSError:
        print("Произошла системная ошибка при попытке открыть файл.")
    except Exception:
        print("Произошла неизвестная ошибка.")


def main():
    input_filename, offset, language = get_cesar_input()

    ALPHABETS = {
        "русский": 'абвгдежзийклмнопрстуфхцчшщъыьэюя',
        "английский": 'abcdefghijklmnopqrstuvwxyz'
    }

    alphabet = ALPHABETS.get(language.lower())
    if alphabet:
        cesar_encrypt_file(input_filename, offset, alphabet)
    else:
        print("Выбран неизвестный язык.")


if __name__ == "__main__":
    main()
