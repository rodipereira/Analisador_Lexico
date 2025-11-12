# Analisador Léxico e Sintático — Checkpoint 2

Aluno: Rodrigo Pereira de Almeida — RGM: 30173591

# Relatório de Desenvolvimento — Analisador Sintático Descendente Preditivo Recursivo

**Projeto de Linguagens de Programação — Prof. Maelso Bruno Pacheco (CCP8A)**  
**Rodrigo Pereira de Almeida — RGM: 30173591**

---

## Visão geral

Este repositório contém o trabalho referente ao Checkpoint 2: a adaptação do analisador léxico e a implementação de um analisador sintático recursivo-descendente (top-down, estilo preditivo). O objetivo foi suportar a gramática solicitada, detectar e anotar erros léxicos e sintáticos sem interromper imediatamente a execução, e gerar evidências para relatório e validação.

## Conteúdo do repositório

- `lexer.py` — varredura do código-fonte, produção de tokens e registro de erros léxicos.
- `parser.py` — analisador recursivo-descendente com acumulação de erros e mecanismo simples de recuperação (panic mode).
- `main.py` — driver que coordena a execução (tokenização + parsing) e imprime as anotações de erro e a lista de tokens.
- `reserved_words.py`, `my_token.py` — utilitários para mapeamento de palavras reservadas e definição de tokens.
- `example_input.txt` — programa de exemplo usado para demonstração (contém linhas intencionais com erros).
- `tests/` — casos de teste (se presentes) para validar comportamentos específicos.

## Principais objetivos implementados

1. Reconhecimento dos tokens exigidos pela gramática do Checkpoint 2: identificadores, `NUMINT`/`NUMREAL`, `CADEIA`, `ASSIGN` (`<-`), `INC`/`DEC`, operadores relacionais e aritméticos, pontuação (`{ } ( ) ; , :`), além das palavras reservadas.
2. Implementação do parser recursivo-descendente (predição por lookahead de 1 token) para as produções principais da gramática.
3. Detecção e anotação de erros léxicos (caracteres inválidos, números malformados, strings não terminadas) e sintáticos (produções inesperadas), sem abortar a análise na primeira ocorrência.
4. Regras específicas: rejeição de identificadores iniciados com caracteres não‑ASCII (ex.: `ç`) e tratamento de números malformados (`1a`, `1.1.1`) como erro léxico.

## Como executar

Abra o PowerShell na pasta do projeto e execute:

```powershell
cd C:\Users\roddy\OneDrive\Desktop\Analisador
python main.py
```

Saída esperada:

- Anotações de erro (se houver): primeiro os erros léxicos, depois os erros de sintaxe; cada erro indica a linha e a coluna.
- Em seguida, a lista de tokens reconhecidos (útil para depuração).

Para gravar a saída em arquivo:

```powershell
python main.py > saida.txt
notepad saida.txt
```

## Interpretação de erros (resumo)

- Erros léxicos: `ERRO: <mensagem> na linha X, coluna Y` — exemplos: `Invalid number format`, `Invalid character: ç`, `Unterminated string literal`.
- Erros sintáticos: listados em "Erros de sintaxe:" com posição aproximada; ex.: `Extra input after program at 38:1`.
- Nota: `a1` é tokenizado como `IDENTIFIER(a1)` (não é número). Se estiver fora do `programa`, provoca erro sintático (ex.: Extra input after program).

## Exemplos de entradas que geram erros

- `x <- 1a;`    → número malformado (erro léxico).
- `s <- "hello;` → string não terminada (erro léxico).
- `çvar <- 10;`  → caractere inválido (erro léxico).
- Inserir `a1` após `}` → demonstra `Extra input after program` (erro sintático).

## Estrutura técnica e decisões de implementação

- Lexer: implementado com funções de `peek()` e `advance()` para controlar posição (linha/coluna); tokens gerados como instâncias de `Token(type, value, line, column)`; erros registrados em `self.errors`.
- Parser: implementado por funções por não-terminal; usa `expect()`/`match()`; `expect()` registra erro e tenta recuperação por sincronização até `;` ou `}` para continuar a análise.
- Recuperação de erros: estratégia de pânico simples para permitir a descoberta de múltiplos erros em um único passe.

## Limitações e trabalhos futuros

- A recuperação sintática é básica e pode falhar em cenários muito complexos; uma estratégia mais robusta pode melhorar a qualidade das mensagens.
- Não há análise semântica (tabela de símbolos, verificação de tipos) — esse seria o próximo passo.
- Melhorias nas mensagens de erro: mostrar a linha completa com um apontador (`^`) na coluna do erro e produzir um arquivo de saída anotado automaticamente.

## Testes

- Rode `python main.py` com diferentes versões de `example_input.txt` (ou arquivos em `tests/`) para verificar a detecção de erros e o comportamento do parser.

## Histórico

- Branch de trabalho: `checkpoint2-restore` (alterações e testes realizados nesta branch).
- Observação: o arquivo de relatório `.docx` foi gerado localmente e posteriormente removido do repositório remoto a pedido do autor; a cópia local foi preservada.

---

Se quiser, eu posso formatar esse relatório em Markdown com imagens e exemplos já prontos para colar no Word, ou gerar um arquivo `example_input.annotado.txt` com comentários contendo as mensagens de erro detectadas. Diga o que prefere.

