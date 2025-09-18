from lexer import Lexer

def print_header():
    print("=" * 80)
    print("🔍 ANALISADOR LÉXICO - COMPILADORES")
    print("=" * 80)
    print("👨‍💻 Desenvolvedor: Rodrigo Pereira de Almeida")
    print("📚 Disciplina: Compiladores")
    print("=" * 80)
    print()

def print_code_preview(code):
    print("📄 CÓDIGO FONTE ANALISADO:")
    print("-" * 50)
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        print(f"{i:2d}| {line}")
    print("-" * 50)
    print()

def print_tokens_table(tokens):
    print("🎯 TOKENS IDENTIFICADOS:")
    print("-" * 80)
    print(f"{'#':<3} {'TIPO':<12} {'VALOR':<15} {'POSIÇÃO':<10} {'DESCRIÇÃO'}")
    print("-" * 80)
    
    for i, token in enumerate(tokens, 1):
        descriptions = {
            'INT': 'Tipo de dados inteiro',
            'FLOAT': 'Tipo de dados decimal',
            'IF': 'Estrutura condicional',
            'ELSE': 'Estrutura condicional',
            'PRINT': 'Função de saída',
            'IDENTIFIER': 'Identificador/Variável',
            'NUMBER': 'Literal numérico',
            'OPERATOR': 'Operador',
            'PUNCTUATION': 'Pontuação'
        }
        
        description = descriptions.get(token.type, 'Token')
        position = f"{token.line}:{token.column}"
        
        print(f"{i:<3} {token.type:<12} {token.value:<15} {position:<10} {description}")
    
    print("-" * 80)
    print()

def print_statistics(tokens):
    print("📊 ESTATÍSTICAS DA ANÁLISE:")
    print("-" * 40)
    
    token_counts = {}
    for token in tokens:
        token_counts[token.type] = token_counts.get(token.type, 0) + 1
    
    print(f"🔢 Total de tokens: {len(tokens)}")
    print(f"📏 Linhas processadas: {max([t.line for t in tokens]) if tokens else 0}")
    print()
    
    print("📈 Distribuição por tipo:")
    for token_type, count in sorted(token_counts.items()):
        percentage = (count / len(tokens)) * 100 if tokens else 0
        print(f"   {token_type:<12}: {count:>3} tokens ({percentage:>5.1f}%)")
    
    print("-" * 40)
    print()

def main():
    print_header()
    
    try:
        with open("example_input.txt", "r", encoding="utf-8") as file:
            code = file.read()
        
        print_code_preview(code)
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        if tokens:
            print_tokens_table(tokens)
            print_statistics(tokens)
        else:
            print("❌ Nenhum token foi encontrado no código.")
            
    except FileNotFoundError:
        print("❌ ERRO: Arquivo 'example_input.txt' não encontrado!")
        print("   Certifique-se de que o arquivo existe no diretório atual.")
    except Exception as e:
        print(str(e))   # agora mostra erros léxicos também
    
    print("✅ Análise concluída!")
    print("=" * 80)

if __name__ == "__main__":
    main()
