import sys
from lexer import tokenize
from parser import Parser

def main():
    print("Database CLI (Variant 5). Для вихода введіть EXIT або натисніть Ctrl+C.")
    buffer = ""

    while True:
        try:
            prompt = "db> " if not buffer else "... "
            line = input(prompt)

            if line.strip().upper() == "EXIT":
                break

            
            if ";" in line:
                cmd_part, _, _ = line.partition(";")
                buffer += " " + cmd_part
                
                full_command = buffer.strip()
                buffer = ""

                if not full_command:
                    continue

                try:
                    tokens = tokenize(full_command)
                    parser = Parser(tokens)
                    ast = parser.parse()
                    print("\nУспішний парсинг! Отриманий AST:")
                    print(f"  {ast}\n")
                except SyntaxError as e:
                    print(f"\nПомилка синтаксиса: {e}\n")
            else:
                buffer += " " + line

        except (KeyboardInterrupt, EOFError):
            print("\nЗавершення роботи.")
            sys.exit(0)

if __name__ == "__main__":
    main()