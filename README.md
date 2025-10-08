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
