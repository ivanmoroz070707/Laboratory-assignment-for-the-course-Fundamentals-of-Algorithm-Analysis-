import sys
from lexer import tokenize
from parser import Parser
from engine import Database

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
    db = Database()
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
                        result = db.command_act(ast)
                        print(f"\n{result}\n")
                    except (SyntaxError, ValueError) as e:
                        print(f"\nПомилка: {e}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nЗавершення роботи.")
            sys.exit(0)

if __name__ == "__main__":
    main()