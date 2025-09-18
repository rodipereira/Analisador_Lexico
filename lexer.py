import re
from my_token import Token
from reserved_words import RESERVED_WORDS

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_line = 1
        self.current_column = 1
        self.pos = 0

    def advance(self):
        if self.pos < len(self.code):
            char = self.code[self.pos]
            self.pos += 1
            self.current_column += 1
            if char == '\n':
                self.current_line += 1
                self.current_column = 1
            return char
        return ''

    def peek(self):
        return self.code[self.pos] if self.pos < len(self.code) else ''

    def add_token(self, type_, value, line, column):
        self.tokens.append(Token(type_, value, line, column))

    def match(self, expected):
        if self.peek() == expected:
            self.advance()
            return True
        return False

    def skip_whitespace(self):
        while self.peek().isspace():
            self.advance()

    def skip_comment(self):
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
        elif self.peek() == '*':
            self.advance()
            while True:
                if self.peek() == '*' and self.pos + 1 < len(self.code) and self.code[self.pos + 1] == '/':
                    self.advance()
                    self.advance()
                    break
                if not self.peek():
                    break
                self.advance()

    def tokenize(self):
        while self.pos < len(self.code):
            current = self.peek()
            line, column = self.current_line, self.current_column

            # Espaços
            if current.isspace():
                self.advance()
                continue

            # Comentário linha única
            if current == '#':
                self.advance()
                while self.peek() != '\n' and self.peek():
                    self.advance()
                continue

            # Comentário de bloco /* ... */
            if current == '/' and self.code[self.pos + 1:self.pos + 2] == '*':
                self.advance()
                self.advance()
                while not (self.peek() == '*' and self.code[self.pos + 1:self.pos + 2] == '/'):
                    if not self.peek():
                        self.error('Unterminated block comment', line, column)
                    self.advance()
                self.advance()
                self.advance()
                continue

            # Identificadores (sem acentos)
            if current.isalpha() or current == '_':
                if not re.match(r"[a-zA-Z_]", current):
                    self.error(f"Invalid identifier start: {current}", line, column)

                identifier = ''
                while re.match(r"[a-zA-Z0-9_]", self.peek()):
                    identifier += self.advance()

                token_type = RESERVED_WORDS.get(identifier, 'IDENTIFIER')
                self.add_token(token_type, identifier, line, column)
                continue

            # Números
            if current.isdigit() or (current == '.' and self.code[self.pos + 1:self.pos + 2].isdigit()):
                number = ''
                dot_count = 0

                if current == '.':
                    number += self.advance()
                    dot_count += 1

                while self.peek().isdigit() or self.peek() == '.':
                    if self.peek() == '.':
                        dot_count += 1
                        if dot_count > 1:  # Mais de um ponto => erro
                            self.error("Invalid number format: multiple decimal points", line, column)
                        number += self.advance()
                        continue
                    number += self.advance()

                if number.endswith('.'):
                    self.error('Invalid number format: ends with dot', line, column)

                if dot_count > 1:
                    continue  # não adiciona token

                self.add_token('NUMBER', number, line, column)
                continue

            # Operadores
            if current in '+-*/=()<>!':
                op = self.advance()
                if op in ['=', '!', '<', '>'] and self.peek() == '=':
                    op += self.advance()
                self.add_token('OPERATOR', op, line, column)
                continue

            # Pontuação
            if current in ';,{}[]':
                punct = self.advance()
                self.add_token('PUNCTUATION', punct, line, column)
                continue

            # Qualquer outro caractere inválido
            self.error(f'Unexpected character: {current}', line, column)

        return self.tokens

    def error(self, message, line, column):
        raise Exception(f"❌ [ERRO LÉXICO] {message} na linha {line}, coluna {column}")
