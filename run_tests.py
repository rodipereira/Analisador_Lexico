import glob
from lexer import Lexer
from parser import Parser, ParseError

files = [
    'tests/test_ok.txt',
    'tests/test_missing_semicolon.txt',
    'tests/test_wrong_assign.txt',
    'tests/test_unclosed_block.txt'
]

for f in files:
    print('\n===', f, '===')
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            code = fh.read()
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        print('Tokens:', [f"{t.type}({t.value})@{t.line}:{t.column}" for t in tokens])
        parser = Parser(tokens)
        try:
            parser.parse()
            print('Result: OK (program syntactically correct)')
        except ParseError as pe:
            print('Syntax error:', pe)
    except FileNotFoundError:
        print('File not found:', f)
    except Exception as e:
        print('Error while testing', f, e)
