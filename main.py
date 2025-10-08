from lexer import Lexer

# Aluno: Rodrigo Pereira de Almeida

def main():
    try:
        with open("example_input.txt", "r", encoding="utf-8") as file:
            code = file.read()
        
        # Cria uma instância do lexer com o código
        lexer = Lexer(code)
        # executa a analise lexica
        tokens = lexer.tokenize()
        
        for token in tokens:
            print(f"{token.type} {token.value} {token.line}:{token.column}")
            
    except FileNotFoundError:
        print("ERRO: Arquivo 'example_input.txt' não encontrado!")
    except Exception as e:
        print(f"ERRO: {e}")

if __name__ == "__main__":
    main()