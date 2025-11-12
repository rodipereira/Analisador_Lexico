from my_token import Token
from reserved_words import RESERVED_WORDS

class Lexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.errors = []
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

    def is_ascii_letter(self, c):
        """Return True for ASCII letters or underscore only (a-z, A-Z, _)."""
        if not c:
            return False
        return c == '_' or ('a' <= c <= 'z') or ('A' <= c <= 'Z')

    def is_ascii_alnum_or_underscore(self, c):
        if not c:
            return False
        return ('0' <= c <= '9') or ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'

    def peek(self):
        return self.code[self.pos] if self.pos < len(self.code) else ''

    def add_token(self, type_, value, line, column):
        self.tokens.append(Token(type_, value, line, column))


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

            if not current:
                break

            if current.isspace():
                self.advance()
                continue

            # Line comment starting with '#'
            if current == '#':
                self.advance()
                while self.peek() and self.peek() != '\n':
                    self.advance()
                continue

            # Block comment: /* ... */
            if current == '/' and self.code[self.pos + 1:self.pos + 2] == '*':
                self.advance(); self.advance()
                while not (self.peek() == '*' and self.code[self.pos + 1:self.pos + 2] == '/'):
                    if not self.peek():
                        self.error('Unterminated block comment', line, column)
                        return self.tokens
                    self.advance()
                self.advance(); self.advance()
                continue

            # Identifiers and reserved words (ASCII letters + underscore only, case-insensitive)
            if self.is_ascii_letter(current):
                identifier = ''
                while self.peek() and self.is_ascii_alnum_or_underscore(self.peek()):
                    identifier += self.advance()
                token_type = RESERVED_WORDS.get(identifier.lower(), 'IDENTIFIER')
                self.add_token(token_type, identifier, line, column)
                continue

            # Numbers: integer or real with a single decimal point
            if current.isdigit() or (current == '.' and self.code[self.pos + 1:self.pos + 2].isdigit()):
                number = ''
                has_dot = False
                if current == '.':
                    number += self.advance()
                    has_dot = True
                    # . must be followed by digit due to the initial check
                while self.peek() and self.peek().isdigit():
                    number += self.advance()

                # optional single fractional part
                if self.peek() == '.' and not has_dot:
                    number += self.advance()
                    has_dot = True
                    if not self.peek().isdigit():
                        # e.g., '1.' is invalid
                        self.error('Invalid number format', line, column)
                        continue
                    while self.peek() and self.peek().isdigit():
                        number += self.advance()

                # If immediately after the numeric sequence follows a letter/underscore or another dot -> invalid
                nxt = self.peek()
                if nxt and (self.is_ascii_letter(nxt) or nxt == '_' or nxt == '.'):
                    # consume the rest of the contiguous invalid sequence to avoid splitting it into tokens
                    while self.peek() and (self.peek().isalnum() or self.peek() in '._'):
                        self.advance()
                    self.error('Invalid number format', line, column)
                    continue

                if number.endswith('.'):
                    self.error('Invalid number format', line, column)
                    continue

                # decide NUMINT or NUMREAL
                if has_dot:
                    self.add_token('NUMREAL', number, line, column)
                else:
                    self.add_token('NUMINT', number, line, column)
                continue

            # Assignment operator '<-'
            if current == '<' and self.code[self.pos + 1:self.pos + 2] == '-':
                self.advance(); self.advance()
                self.add_token('ASSIGN', '<-', line, column)
                continue

            # Increment/Decrement
            if current == '+' and self.code[self.pos + 1:self.pos + 2] == '+':
                self.advance(); self.advance()
                self.add_token('INC', '++', line, column)
                continue
            if current == '-' and self.code[self.pos + 1:self.pos + 2] == '-':
                self.advance(); self.advance()
                self.add_token('DEC', '--', line, column)
                continue

            # Operators (including relational): + - * / == != <= >= < >
            if current in '+-*/=<>!':
                op = self.advance()
                if op in ['=', '!', '<', '>'] and self.peek() == '=':
                    op += self.advance()
                self.add_token('OPERATOR', op, line, column)
                continue

            # Punctuation specific tokens
            if current == '(':
                self.advance(); self.add_token('LPAREN', '(', line, column); continue
            if current == ')':
                self.advance(); self.add_token('RPAREN', ')', line, column); continue
            if current == '{':
                self.advance(); self.add_token('LBRACE', '{', line, column); continue
            if current == '}':
                self.advance(); self.add_token('RBRACE', '}', line, column); continue
            if current == ';':
                self.advance(); self.add_token('SEMICOLON', ';', line, column); continue
            if current == ',':
                self.advance(); self.add_token('COMMA', ',', line, column); continue
            if current == ':':
                self.advance(); self.add_token('COLON', ':', line, column); continue

            # String literals (CADEIA)
            if current == '"':
                self.advance()
                string_val = ''
                while self.peek() and self.peek() != '"':
                    # simple support for escaped quotes could be added here
                    string_val += self.advance()
                if self.peek() != '"':
                    self.error('Unterminated string literal', line, column)
                    continue
                self.advance()  # consume closing quote
                self.add_token('CADEIA', string_val, line, column)
                continue

            # Specific disallowed characters (example)
            if current in ('ç', '@'):
                self.error(f'Invalid character: {current}', line, column)
                self.advance()
                continue

            # Anything else is unexpected
            self.error(f'Unexpected character: {current}', line, column)
            self.advance()

        return self.tokens

    def error(self, message, line, column):
        # record and print lexical errors
        msg = f"ERRO: {message} na linha {line}, coluna {column}"
        self.errors.append(msg)
        print(msg)