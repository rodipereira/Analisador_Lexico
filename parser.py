class ParseError(Exception):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def match(self, type_, value=None):
        tok = self.peek()
        if not tok:
            return False
        if tok.type != type_:
            return False
        if value is not None and tok.value != value:
            return False
        self.advance()
        return True

    def expect(self, type_, value=None):
        tok = self.peek()
        if not tok:
            self.error(f"Unexpected end of input, expected {type_} {value if value else ''}", tok)
            return None
        if tok.type != type_ or (value is not None and tok.value != value):
            self.error(f"Expected {type_} {value if value else ''}, got {tok.type}({tok.value})", tok)
            # Attempt simple recovery: look ahead for the expected token before a statement terminator
            i = self.pos
            found = False
            while i < len(self.tokens):
                if self.tokens[i].type == type_ and (value is None or self.tokens[i].value == value):
                    found = True
                    break
                if self.tokens[i].type in ('SEMICOLON', 'RBRACE'):
                    break
                i += 1
            if found:
                # skip until the expected token and consume it
                while self.pos < i:
                    self.advance()
                return self.advance()
            # otherwise synchronize to next statement boundary
            self.synchronize()
            return None
        return self.advance()

    def error(self, message, tok=None):
        if tok:
            msg = f"Syntax error: {message} at {tok.line}:{tok.column}"
        else:
            msg = f"Syntax error: {message}"
        self.errors.append(msg)
        print(msg)

    def synchronize(self, sync_tokens=('SEMICOLON', 'RBRACE')):
        tok = self.peek()
        while tok and tok.type not in sync_tokens:
            self.advance()
            tok = self.peek()
        # optionally consume the sync token to move past the statement
        if self.peek() and self.peek().type in sync_tokens:
            self.advance()

    # Grammar implementation
    def parse(self):
        self.programa()
        if self.peek() is not None:
            tok = self.peek()
            self.error(f"Extra input after program", tok)
        return len(self.errors) == 0

    def programa(self):
        # programa : 'main' '{' corpo '}'
        self.expect('MAIN')
        self.expect('LBRACE')
        self.corpo()
        self.expect('RBRACE')

    def corpo(self):
        # corpo : secaoDeclaracoes listaComandos
        self.secaoDeclaracoes()
        self.listaComandos()

    def secaoDeclaracoes(self):
        # secaoDeclaracoes : 'var' '{' listaDeclaracoes '}'
        self.expect('VAR')
        self.expect('LBRACE')
        self.listaDeclaracoes()
        self.expect('RBRACE')

    def listaDeclaracoes(self):
        # listaDeclaracoes : declaracao listaDeclaracoes | declaracao
        # implement as one or more declaracao until RBRACE
        while True:
            if self.peek() and self.peek().type == 'IDENTIFIER':
                self.declaracao()
            else:
                break

    def declaracao(self):
        # declaracao : ID ':' tipo ';'
        self.expect('IDENTIFIER')
        self.expect('COLON')
        self.tipo()
        self.expect('SEMICOLON')

    def tipo(self):
        # tipo : 'int' | 'real'
        if self.match('INT'):
            return
        if self.match('REAL'):
            return
        tok = self.peek()
        self.error("Expected type int or real", tok)
        # try to recover
        self.synchronize()
        return

    def listaComandos(self):
        # listaComandos : comando listaComandos | comando
        # implement as zero or more comandos until RBRACE or EOF
        while True:
            tok = self.peek()
            if not tok or tok.type == 'RBRACE':
                break
            self.comando()

    def comando(self):
        # comando : atribuicao | leitura | escrita | condicional | repeticao | bloco
        tok = self.peek()
        if not tok:
            self.error('Unexpected end of input in comando', tok)
            return
        if tok.type == 'IDENTIFIER':
            # could be atribuicao
            self.atribuicao()
        elif tok.type == 'INPUT':
            self.leitura()
        elif tok.type == 'PRINT':
            self.escrita()
        elif tok.type == 'IF':
            self.condicional()
        elif tok.type == 'WHILE':
            self.repeticao()
        elif tok.type == 'LBRACE':
            self.bloco()
        else:
            self.error(f"Unexpected token in comando: {tok.type}({tok.value})", tok)
            # try to recover to next statement
            self.synchronize()
            return

    def atribuicao(self):
        # atribuicao : ID '<-' expressaoAritmetica ';'
        self.expect('IDENTIFIER')
        self.expect('ASSIGN')
        self.expressaoAritmetica()
        self.expect('SEMICOLON')

    def leitura(self):
        # leitura : 'input(' ID ')' ';'
        self.expect('INPUT')
        self.expect('LPAREN')
        self.expect('IDENTIFIER')
        self.expect('RPAREN')
        self.expect('SEMICOLON')

    def escrita(self):
        # escrita : 'print(' (ID | CADEIA) ')' ';'
        self.expect('PRINT')
        self.expect('LPAREN')
        tok = self.peek()
        if tok and tok.type == 'IDENTIFIER':
            self.advance()
        elif tok and tok.type == 'CADEIA':
            self.advance()
        else:
            self.error(f"Expected IDENTIFIER or CADEIA in print", tok)
            self.synchronize()
            return
        self.expect('RPAREN')
        self.expect('SEMICOLON')

    def condicional(self):
        # condicional : 'if' expressaoRelacional 'then' comando [ 'else' comando ]
        self.expect('IF')
        self.expressaoRelacional()
        self.expect('THEN')
        self.comando()
        if self.match('ELSE'):
            self.comando()

    def repeticao(self):
        # repeticao : 'while' expressaoRelacional comando
        self.expect('WHILE')
        self.expressaoRelacional()
        self.comando()

    def bloco(self):
        # bloco : '{' listaComandos '}'
        self.expect('LBRACE')
        self.listaComandos()
        self.expect('RBRACE')

    # Expressions
    def expressaoAritmetica(self):
        # implemented as expr -> term ((+|-) term)*
        self.term()
        while True:
            tok = self.peek()
            if tok and tok.type == 'OPERATOR' and tok.value in ('+', '-'):
                self.advance()
                self.term()
            else:
                break

    def term(self):
        # term -> factor ((*|/) factor)*
        self.fator()
        while True:
            tok = self.peek()
            if tok and tok.type == 'OPERATOR' and tok.value in ('*', '/'):
                self.advance()
                self.fator()
            else:
                break

    def fator(self):
        tok = self.peek()
        if not tok:
            self.error('Unexpected end of input in fator', tok)
            return
        if tok.type == 'NUMINT' or tok.type == 'NUMREAL':
            self.advance(); return
        if tok.type == 'IDENTIFIER':
            # could be ID ++ or ID --
            self.advance()
            nxt = self.peek()
            if nxt and nxt.type in ('INC', 'DEC'):
                self.advance()
            return
        if tok.type == 'LPAREN':
            self.advance()
            self.expressaoAritmetica()
            self.expect('RPAREN')
            return
        self.error(f"Unexpected token in fator: {tok.type}({tok.value})", tok)
        # try to recover
        self.synchronize()
        return

    def expressaoRelacional(self):
        # handle NOT unary
        tok = self.peek()
        if tok and tok.type == 'NOT':
            self.advance()
            self.expressaoRelacional()
            return
        # parse termoRelacional then optional logical operators
        self.termoRelacional()
        while True:
            tok = self.peek()
            if tok and tok.type in ('AND', 'OR'):
                self.advance()
                self.termoRelacional()
            else:
                break

    def termoRelacional(self):
        tok = self.peek()
        if tok and tok.type == 'LPAREN':
            self.advance()
            self.expressaoRelacional()
            self.expect('RPAREN')
            return
        # expect expressaoAritmetica OP_REL expressaoAritmetica
        self.expressaoAritmetica()
        tok = self.peek()
        if tok and tok.type == 'OPERATOR' and tok.value in ('>', '<', '>=', '<=', '==', '!='):
            self.advance()
            self.expressaoAritmetica()
            return
        self.error((f"Expected relational operator at {tok.line}:{tok.column}" if tok else "Unexpected end in termoRelacional"), tok)
        self.synchronize()
        return