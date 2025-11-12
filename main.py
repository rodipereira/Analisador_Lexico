from lexer import Lexer
from parser import Parser

# Aluno: Rodrigo Pereira de Almeida

def main():
    # prefer program file if present
    filename = "example_input.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            code = file.read()

        lexer = Lexer(code)
        tokens = lexer.tokenize()

        # build parser and run it even if lexical errors occurred so we annotate syntax errors
        parser = Parser(tokens)
        parser.parse()

        # Print all errors first (lexical then syntax) so they appear at the top as annotations
        if getattr(lexer, 'errors', None) or getattr(parser, 'errors', None):
            print('\n--- Erros encontrados (anotados) ---')
            if getattr(lexer, 'errors', None):
                print('\nErros léxicos:')
                for e in lexer.errors:
                    print(e)
            if getattr(parser, 'errors', None):
                print('\nErros de sintaxe:')
                for e in parser.errors:
                    print(e)
            print('--- Fim dos erros ---\n')
        else:
            print("Parsing succeeded: programa válido.")

        # print tokens (optional, after errors) — useful for debugging/annotations
        for token in tokens:
            print(f"{token.type}({token.value}) at {token.line}:{token.column}")

    except FileNotFoundError:
        print(f"ERRO: Arquivo '{filename}' não encontrado!")
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    main()