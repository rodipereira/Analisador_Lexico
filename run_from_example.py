from lexer import Lexer
from parser import Parser, ParseError

def load_sections(filename):
    sections = []
    current_name = None
    current_lines = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip().startswith('// ==='):
                if current_name:
                    sections.append((current_name, ''.join(current_lines)))
                # parse name from comment
                current_name = line.strip().lstrip('//').strip()
                current_lines = []
            else:
                current_lines.append(line)
        if current_name:
            sections.append((current_name, ''.join(current_lines)))
    return sections


def run_section(name, code):
    print('\n===', name, '===')
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    if tokens:
        print('Tokens sample:', [f"{t.type}({t.value})@{t.line}:{t.column}" for t in tokens[:30]])
    else:
        print('No tokens produced.')
    parser = Parser(tokens)
    try:
        parser.parse()
        print('Result: OK (program syntactically correct)')
        return True, None
    except ParseError as pe:
        print('Syntax error:', pe)
        return False, str(pe)
    except Exception as e:
        print('Error during parsing:', e)
        return False, str(e)


if __name__ == '__main__':
    sections = load_sections('example_input.txt')
    results = {}
    for name, code in sections:
        ok, err = run_section(name, code)
        results[name] = (ok, err)

    print('\nSummary:')
    for name, (ok, err) in results.items():
        print(f"{name}: {'OK' if ok else 'ERROR'}")
