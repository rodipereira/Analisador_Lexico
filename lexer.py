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

            if current.isspace():
                self.advance()
                continue

            if current == '#':
                self.advance()
                while self.peek() != '\n' and self.peek():
                    self.advance()
                continue

            if current == '/' and self.code[self.pos + 1:self.pos + 2] == '*':
                self.advance()
                self.advance()
                while not (self.peek() == '*' and self.code[self.pos + 1:self.pos + 2] == '/'):
                    if not self.peek():
                        self.error('Unterminated block comment', line, column)
                        return
                    self.advance()
                self.advance()
                self.advance()
                continue

            if current.isalpha() or current == '_':
                identifier = ''
                while self.peek().isalnum() or self.peek() == '_':
                    identifier += self.advance()
                token_type = RESERVED_WORDS.get(identifier, 'IDENTIFIER')
                self.add_token(token_type, identifier, line, column)
                continue

            if current.isdigit() or (current == '.' and self.code[self.pos + 1:self.pos + 2].isdigit()):
                number = ''
                has_dot = False
                if current == '.':
                    number += self.advance()
                    has_dot = True
                while self.peek().isdigit():
                    number += self.advance()
                if self.peek() == '.' and not has_dot:
                    number += self.advance()
                    has_dot = True
                    if not self.peek().isdigit():
                        self.error('Invalid number format', line, column)
                        continue
                    while self.peek().isdigit():
                        number += self.advance()
                # CORREÇÃO: Detectar múltiplos pontos decimais
                elif self.peek() == '.' and has_dot:
                    self.error('Invalid number format: multiple decimal points', line, column)
                    self.advance()  # Consumir o ponto inválido
                    continue
                if number.endswith('.'):
                    self.error('Invalid number format: number ending with decimal point', line, column)
                    continue
                self.add_token('NUMBER', number, line, column)
                continue

            if current in '+-*/=()<>!':
                op = self.advance()
                if op in ['=', '!', '<', '>'] and self.peek() == '=':
                    op += self.advance()
                self.add_token('OPERATOR', op, line, column)
                continue

            # Punctuation: semicolon, comma, braces, brackets
            if current in ';,{}[]':
                punct = self.advance()
                self.add_token('PUNCTUATION', punct, line, column)
                continue

            # Detectar caracteres inválidos específicos
            if current == 'ç':
                self.error('Invalid character: ç (not allowed)', line, column)
                self.advance()
                continue
            
            if current == '@':
                self.error('Invalid character: @ (not allowed)', line, column)
                self.advance()
                continue

            self.error(f'Unexpected character: {current}', line, column)
            self.advance()

        return self.tokens

    def error(self, message, line, column):
        print(f"ERRO: {message} na linha {line}, coluna {column}")
