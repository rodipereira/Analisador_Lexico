from lexer import Lexer
from parser import Parser, ParseError

# Aluno: Rodrigo Pereira de Almeida

def main():
    # prefer program file if present
    filename = "programa_ckp2_qui_noite.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            code = file.read()

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # print tokens (optional)
        for token in tokens:
            print(f"{token.type}({token.value}) at {token.line}:{token.column}")

        # parse
        parser = Parser(tokens)
        try:
            parser.parse()
            print("Parsing succeeded: programa válido.")
        except ParseError as pe:
            print(f"Syntax error: {pe}")

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    main()