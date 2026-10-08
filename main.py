import sys
from lexer import tokenize
from parser import Parser

def split_unquoted_semicolon(text: str):

    in_quotes = False
    for i, char in enumerate(text):
        if char == '"':
            in_quotes = not in_quotes
        elif char == ';' and not in_quotes:
            return text[:i], text[i+1:]
    return None, text

def main():
    print("Database CLI (Variant 5). Для виходу введіть EXIT або натисніть Ctrl+C.")
    buffer = ""

    while True:
        try:
            prompt = "db> " if not buffer else "... "
            line = input(prompt)

            if line.strip().upper() == "EXIT":
                break

           
            buffer += (" " if buffer else "") + line

            
            while True:
                cmd_part, rest = split_unquoted_semicolon(buffer)
                if cmd_part is None:
                    break

                full_command = cmd_part.strip()
                buffer = rest

                if full_command:
                    try:
                        tokens = tokenize(full_command)
                        parser = Parser(tokens)
                        ast = parser.parse()
                        print("\nУспішний парсинг! Отриманий AST:")
                        print(f"  {ast}\n")
                    except SyntaxError as e:
                        print(f"\nПомилка синтаксису: {e}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nЗавершення роботи.")
            sys.exit(0)

if __name__ == "__main__":
    main()