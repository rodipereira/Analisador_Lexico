# Analisador Léxico e Sintático — Checkpoint 2

Aluno: Rodrigo Pereira de Almeida — RGM: 30173591

Branch de trabalho: `checkpoint2-restore`

## Visão Geral
Este repositório contém um analisador léxico e um analisador sintático recursivo-descendente (top-down, estilo preditivo) para a gramática do Checkpoint 2. O projeto inclui tratamento de erros léxicos e sintáticos que são anotados e exibidos sem abortar imediatamente a execução, facilitando a geração de evidências para relatório.

## Estrutura principal
- `lexer.py` — scanner que produz tokens e registra erros léxicos (`self.errors`).
- `parser.py` — analisador recursivo-descendente; registra erros sintáticos e tenta recuperação (panic mode).
- `main.py` — driver que lê `example_input.txt`, chama o lexer e o parser, e imprime anotações de erro e tokens.
- `reserved_words.py`, `my_token.py` — utilitários para tokens e palavras reservadas.
- `example_input.txt` — programa de exemplo (contém linhas intencionais com erros para demonstração).
- `tests/` — arquivos de teste com vários cenários (se presentes).

## Requisitos
- Python 3.11+ (testado em 3.13).
- Dependências opcionais (apenas para geração do .docx de relatório): `python-docx` (instalação com pip abaixo).

## Instalação rápida
Abra PowerShell na pasta do projeto:

```powershell
cd C:\Users\roddy\OneDrive\Desktop\Analisador
python -m pip install --user python-docx
```

Observação: `python-docx` é somente necessário se você for gerar o .docx do relatório. O analisador funciona sem essa biblioteca.

## Como executar
No PowerShell, execute:

```powershell
python main.py
```

Saída esperada:
- Primeiro serão impressas as anotações de erro (se houver): erros léxicos e, em seguida, erros de sintaxe.
- Depois será listada a sequência de tokens reconhecidos (útil para depuração).

Para salvar a saída em arquivo:

```powershell
python main.py > saida.txt
notepad saida.txt
```

## Interpretando erros
- Erros léxicos: aparecem no formato `ERRO: <mensagem> na linha X, coluna Y`. Exemplos: `Invalid number format`, `Invalid character: ç`, `Unterminated string literal`.
- Erros sintáticos: aparecem como mensagens listadas em "Erros de sintaxe:". Exemplos: `Extra input after program at L:C`, `Expected IDENTIFIER or CADEIA in print at L:C`.
- Observação: `a1` não é um número; é tokenizado como `IDENTIFIER(a1)` — pode causar erro sintático se estiver fora do `programa`.

## Criar casos de teste
- Coloque arquivos com trechos de teste em `tests/` e rode o analisador apontando para esses arquivos ou abra/edite `example_input.txt` com os casos desejados.

Exemplos de erros para inserir em `example_input.txt`:
- `x <- 1a;`    # número malformado — erro léxico
- `s <- "hello;` # string não terminada — erro léxico
- `çvar <- 10;`  # caractere inválido — erro léxico
- Colocar `a1` após o `}` final do `programa` para demonstrar `Extra input after program` (erro sintático)

## Produzir arquivo de saída anotado (opcional)
Se quiser que o analisador gere um arquivo com as anotações (por exemplo `saida_anotada.txt`), posso adicionar essa opção ao `main.py` sob pedido.

## Histórico / Observações
- O relatório em `.docx` foi gerado localmente e posteriormente removido do repositório remoto a pedido do autor (arquivo local preservado). Se precisar que ele seja re-adicionado, posso fazê-lo.
- A branch de trabalho usada para entrega deste checkpoint é `checkpoint2-restore`.

## Contato
Se tiver dúvidas ou quiser que eu gere os prints/anotações automaticamente, diga como prefere (arquivo anotado, runner de testes, ou geração de imagens).

---
Arquivo gerado automaticamente por assistência. Copie este README para o Word ou mantenha-o no repositório como referência.
# Analisador Léxico - Python

## Desenvolvedor
- Rodrigo Pereira de Almeida

## Como executar

1. Certifique-se de ter Python 3 instalado.
2. Coloque um código de exemplo em `example_input.txt`.
3. Execute o programa com:

```bash
python main.py
```

O analisador exibirá os tokens reconhecidos no terminal.

## Requisitos implementados
Todos os itens do Checkpoint 01 foram implementados conforme solicitado.

## Funcionalidades implementadas
- ✅ Reconhecimento de identificadores e palavras reservadas
- ✅ Análise de números inteiros e decimais
- ✅ Detecção de operadores simples e compostos (+, -, *, /, =, ==, !=, <=, >=)
- ✅ Tratamento de comentários de linha (#) e bloco (/* */)
- ✅ Reconhecimento de pontuação (;, {}, [], etc.)
- ✅ Validação rigorosa de números decimais (rejeita múltiplos pontos)
- ✅ Interface amigável com tabelas e estatísticas
- ✅ Tratamento de erros com mensagens claras

## Correções implementadas
- **Bug fix**: Corrigido problema de validação de números decimais múltiplos
  - Antes: `1.01.1` era aceito incorretamente
  - Agora: Números com múltiplos pontos decimais são rejeitados com erro específico

## Alterações recentes (resumo básico)
- O analisador agora trata chaves e pontuação (`{ } ; , [ ]`) como tokens de pontuação.
- Números do tipo `1a` ou sequências com vários pontos (`1.1.1.1`) são considerados erro léxico e não são divididos em tokens válidos.
- Removido método não utilizado `match()` do lexer.
