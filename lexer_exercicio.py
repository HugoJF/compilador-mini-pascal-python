import re
import pprint


class AnaLex:
    # List of reserved tokens
    reserved_tokens = []

    # List containing the order for rule execution
    rules_order = []

    # The matching rules
    rules = {}

    # Input to be matched
    code = ''

    # Where the analysis is inside the code
    i = 0

    # Line counter
    lineno = 1

    # Getters
    def set_code_input(self, code):
        self.code = code

    def set_reserved_tokens(self, reserved):
        self.reserved_tokens = reserved

    def set_rules(self, rules):
        self.rules = rules

    def set_rules_order(self, rules_order):
        self.rules_order = rules_order

    # TODO: Check if rules are correctly defined
    def check_rules(self):
        return True

    # Check if rules order list contains every defined rule
    def check_rules_order(self):
        # Check if user set the execution order on every token
        tokenSet = set(self.rules.keys())
        orderSet = set(self.rules_order)
        intersect = tokenSet.intersection(orderSet)

        if len(intersect) != len(tokenSet):
            return False
        else:
            return True

    # Compile regex definitions
    def compile(self):
        for token in self.rules_order:
            info = self.rules[token]
            info['compiled'] = re.compile(info['regex'])

        return True

    # If matching reached end of file
    def ended(self):
        return self.i >= len(self.code)

    # Returns next match
    def next(self):
        if self.ended():
            return False

        tokenType = None
        match = None
        # Tries to match any token compiled regex
        for token in self.rules_order:
            info = self.rules[token]
            match = info['compiled'].match(self.code, self.i)

            # If any match is found, stop trying
            if match:

                # If we have a custom validation rule, call it
                if 'validation' in info and callable(info['validation']):
                    valid = info['validation'](self, match.group())
                    if not valid:
                        continue

                tokenType = token
                break
        # If we have a match, output it, else output error
        if match:
            # Should we check for newlines?
            if 'newline' in self.rules[token]:
                # The number of lines this match will add to line counter
                newline_count = 0
                # Token new line parameter
                newline = self.rules[token].get('newline', False)

                # Check if token has custom function for new lines (function)
                if callable(newline):
                    newline_count = newline(self, match.group())
                # Check if token has fixed new line amount (int)
                elif isinstance(newline, int):
                    newline_count += newline
                # Check if token jumps a line (boolean)
                elif newline == True:
                    newline_count = 1

                # Jumps lines
                self.lineno += newline_count

            # Output match?
            if self.rules[token].get('ignore', False) != True:
                # Default matches to not have attributes
                attrib = False

                # Checks if token type has attributes
                if 'has_attribute' in self.rules[token]:
                    # Cache parameter reference
                    has_attribute = self.rules[token].get('has_attribute', False)

                    # Calls custom function to determine if token has attributes
                    if callable(has_attribute):
                        attrib = has_attribute(self, match.group())
                    elif isinstance(has_attribute, bool):
                        attrib = has_attribute

                if attrib:
                    # If match has attributes, print with it
                    # print ('< {}, {}, {} >'.format(self.lineno, token, match.group()))
                    pass
                else:
                    if match.group().upper() in self.reserved_tokens:
                        # If match is reserved token, the token name is the reserved token name
                        # print ('< {}, {} >'.format(self.lineno, match.group().upper()))
                        pass
                    else:
                        # If match is not a reserved token, print token type
                        # print ('< {}, {} >'.format(self.lineno, token))
                        pass
            # Advance matching index to the end of current match (avoids matching inside current matched token)
            self.i += len(match.group())
        else:
            # If we could not find a match, throw lexic error
            # print('< {}, {} >'.format(self.lineno, 'ERRO_LEXICO'))
            pass
            # Advance matching index
            self.i += 1

            exit()

        return self.lineno, token, match.group().upper()


reserved_tokens = [
    'AND',
    'ARRAY',
    'BEGIN',
    'BOOLEAN',
    'CHAR',
    'DIV',
    'DO',
    'ELSE',
    'END',
    'FALSE',
    'FUNCTION',
    'IF',
    'INTEGER',
    'NOT',
    'OF',
    'OR',
    'PROCEDURE',
    'PROGRAM',
    'READ',
    'THEN',
    'TRUE',
    'VAR',
    'WHILE',
    'WRITE'
]


# Custom validators

def int_newline(lexer, input):
    return int(input)


def id_has_attribute(lexer, id):
    return id.upper() not in lexer.reserved_tokens


def comment_newlines(lexer, comment):
    return comment.count("\n")


# Easy way to keep the order of tokens (since dictionaries cannot guarantee the insertion order)
ordered_rules = [
    'COMMENT',
    'SINGLE_COMMENT',
    'NUM',
    'ASSIGN_OP',
    'GE',
    'RP',
    'LP',
    'GT',
    'LE',
    'DOTDOT',
    'NE',
    'TIMES',
    'LT',
    'SEMICOLON',
    'COMMA',
    'MINUS',
    'COLON',
    'PLUS',
    'DOT',
    'LB',
    'RB',
    'SINGLE_QUOTE',
    'DOUBLE_QUOTE',
    'EQUAL',
    'IDENTIFIER',
    'SPACE',
    'TAB',
    'NEW_LINE'
]

# Define each token using a dictionary
#   Properties:
#     'ignore' : Supress console output when matched
#     'newline': Count a new line when matched
rules = {
    'ASSIGN_OP': {
        'regex': r':='
    },
    'GE': {
        'regex': '>='
    },
    'RP': {
        'regex': '\)'
    },
    'GT': {
        'regex': '>'
    },
    'LE': {
        'regex': '<='
    },
    'LP': {
        'regex': '\('
    },
    'DOTDOT': {
        'regex': '\.\.'
    },
    'NE': {
        'regex': '<>'
    },
    'TIMES': {
        'regex': '\*'
    },
    'LT': {
        'regex': '<'
    },
    'SEMICOLON': {
        'regex': ';'
    },
    'COMMA': {
        'regex': ','
    },
    'MINUS': {
        'regex': '-'
    },
    'COLON': {
        'regex': ':'
    },
    'PLUS': {
        'regex': '\+'
    },
    'DOT': {
        'regex': '\.'
    },
    'LB': {
        'regex': '\['
    },
    'RB': {
        'regex': '\]'
    },
    'EQUAL': {
        'regex': r'='
    },
    'SINGLE_QUOTE': {
        'regex': r'\''
    },
    "DOUBLE_QUOTE": {
        'regex': r'\"'
    },
    'IDENTIFIER': {
        'regex': r'[a-zA-Z][a-zA-Z0-9]*',
        'has_attribute': id_has_attribute
    },
    'COMMENT': {
        'regex': r'(\(\*(?:(?:[\n\t]|[ \S])(?!\/\*))*\*\))',
        'ignore': True,
        'newline': comment_newlines
    },
    'SINGLE_COMMENT': {
        'regex': r'{.*}',
        'ignore': True,
    },
    'NUM': {
        'regex': r'\d+(?:\d+)*(?:[Ee][+-]?\d+)?',
        'has_attribute': True
    },
    'SPACE': {
        'regex': r'[ ]',
        'ignore': True,
    },
    'TAB': {
        'regex': r'\t',
        'ignore': True,
    },
    'NEW_LINE': {
        'regex': r'\r??\n',
        'ignore': True,
        'newline': True,
    }
}

# run.codes
# filename = input()
filename = "test4.pas"
code = ''
with open(filename, 'r') as myfile:
    code = myfile.read()

lexer = AnaLex()
lexer.set_code_input(code)
lexer.set_reserved_tokens(reserved_tokens)
lexer.set_rules(rules)
lexer.set_rules_order(ordered_rules)

lexer.check_rules()
lexer.check_rules_order()

lexer.compile()

actual = None
error = False
current_scope = 0
generated_code = []

symbol_table = {}
label_index = -1


def next_label():
    global label_index
    label_index += 1
    return "L" + str(label_index)


def generate_code(label, command, p1, p2, p3):
    generated_code.append({
        'label': label,
        'command': command,
        'p1': p1,
        'p2': p2,
        'p3': p3,
    })


def get_st(symbol):
    for id, data in symbol_table.items():
        if data['id'] == symbol:
            return data

    return None


def render_code():
    for l in generated_code:
        if 'label' in l and l['label'] is not None:
            print(l['label'] + ': ', end='')
        if 'command' in l and l['command'] is not None:
            print(l['command'], end='')
        if 'p1' in l and l['p1'] is not None:
            print(' ' + str(l['p1']), end='')
        if 'p2' in l and l['p2'] is not None:
            print(', ' + str(l['p2']), end='')
        if 'p3' in l and l['p3'] is not None:
            print(', ' + str(l['p3']), end='')

        print()


def add_st(symbol):
    if symbol['id'] in symbol_table:
        print("Re-declaring symbol", symbol.id)
        error()

    symbol_table[symbol['id']] = symbol


def error(message):
    global actual
    error = True
    print(message, "ACTUAL TOKEN: ", actual, 'AT LINE:', lexer.lineno)
    # raise TypeError("UNEXPECTED ERROR")
    exit()


def match(a, actual):
    reserved = actual[2] in reserved_tokens;
    matched = False

    if reserved:
        matched = actual[2] == a
    else:
        matched = actual[1] == a

    return matched


def lookahead(c):
    global actual
    if match(c, actual):
        return True
    else:
        return False


def multi_lookahead(c):
    global actual
    matched = False
    for x in c:
        if match(x, actual):
            matched = True

    return matched


def consume_token(c):
    global actual

    if match(c, actual):
        # print('Consuming:', c)
        if not lexer.ended():
            actual = lexer.next()
            while 'ignore' in rules[actual[1]] and rules[actual[1]]['ignore'] == True:
                actual = lexer.next()
            # print("Next token is", actual)
            return True
        else:
            return True
    return False


def expect_token(c):
    if consume_token(c):
        return True
    else:
        error(c)
        return False


def program():
    expect_token("PROGRAM")
    generate_code(None, "INPP", None, None, None)
    identifier()
    expect_token("SEMICOLON")
    block()
    expect_token("DOT")


def block():
    variable_declaration_part()
    statement_part()


def variable_declaration_part():
    if consume_token("VAR"):
        offset = 0
        allocations = 0
        if lookahead("IDENTIFIER"):
            while lookahead("IDENTIFIER"):  # deve gerar erro se nao achar identifier
                (offset, allocations) = variable_declaration(offset, allocations)
                expect_token("SEMICOLON")
            generate_code(None, "AMEM", allocations, None, None)
        else:
            error("Expected IDENTIFIER")


def variable_declaration(offset, allocations):
    declarations = []
    busca = get_st(actual[2])
    if busca != None and ('scope' not in busca or busca['scope'] == current_scope):
        error("Re-declaration on same scope")
    add_st({
        'id': actual[2],
        'category': 'VARS',
        'scope': current_scope,
        'type': None,
        'offset': offset,
    })
    declarations.append(actual[2])
    offset = offset + 1
    allocations = allocations + 1
    identifier()
    while consume_token("COMMA"):
        busca = get_st(actual[2])
        if busca != None and ('scope' not in busca or busca['scope'] == current_scope):
            error("Re-declaration on same scope\n")
        add_st({
            'id': actual[2],
            'category': 'VARS',
            'scope': current_scope,
            'type': None,
            'offset': offset,
        })
        declarations.append(actual[2])
        offset = offset + 1
        allocations = allocations + 1
        identifier()
    expect_token("COLON")
    for var in declarations:
        if actual[2].lower() == 'INTEGER'.lower():
            get_st(var)['type'] = 'integer'
        elif actual[2].lower() == 'BOOLEAN'.lower():
            get_st(var)['type'] = 'boolean'
        else:
            error('unrecognized variable type\n')

    type()
    return offset, allocations


def type():
    if multi_lookahead(["CHAR", "INTEGER", "BOOLEAN"]):
        simple_type()
    elif lookahead("ARRAY"):
        array_type()
    else:
        error("Expecting CHAR, INTEGER, BOOLEAN or ARRAY")


def array_type():
    expect_token("ARRAY")
    expect_token("LB")
    index_range()
    expect_token("RB")
    expect_token("OF")
    simple_type()


def index_range():
    integer_constant()
    expect_token("DOTDOT")
    integer_constant()


def simple_type():
    if consume_token("CHAR"):
        pass
    elif consume_token("INTEGER"):
        pass
    elif consume_token("BOOLEAN"):
        pass
    else:
        error("Expecting CHAR, INTEGER or BOOLEAN")


def type_indetifier():
    identifier()


def statement_part():
    compound_statement()


def compound_statement():
    global current_scope
    expect_token("BEGIN")
    current_scope = current_scope + 1
    statement()
    while consume_token("SEMICOLON"):
        statement()
    current_scope = current_scope - 1
    expect_token("END")


def statement():
    if multi_lookahead(["IDENTIFIER", "READ", "WRITE"]):
        simple_statement()
    elif multi_lookahead(["BEGIN", "IF", "WHILE"]):
        structured_statement()
    else:
        error("Expected IDENTIFIER or BEGIN")


def simple_statement():
    if lookahead("IDENTIFIER"):
        assignment_statement()
    elif lookahead("READ"):
        read_statement()
    elif lookahead("WRITE"):
        write_statement()
    else:
        error("Expecting IDENTIFIER, READ or WRITE")


def assignment_statement():
    k = get_st(actual[2])
    if k == None:
        error("Undeclared variable")

    variable()
    expect_token("ASSIGN_OP")
    expression()

    if k['category'] == 'VARS':
        generate_code(None, "ARMZ", k['scope'], k['offset'], None)
    else:
        error("unrecognized variable category")


def read_statement():
    expect_token("READ")

    expect_token("LP")
    k = get_st(actual[2])
    if k == None:
        error("Variable not declared")
    generate_code(None, "LEIT", None, None, None)
    generate_code(None, "ARMZ", k['scope'], k['offset'], None)

    variable()
    while lookahead("COMMA"):
        expect_token("COMMA")

        k = get_st(actual[2])
        if k == None:
            error("Variable not declared")
        generate_code(None, "LEIT", None, None, None)
        generate_code(None, "ARMZ", k['scope'], k['offset'], None)

        variable()
    expect_token("RP")


def write_statement():
    expect_token("WRITE")
    expect_token("LP")

    k = get_st(actual[2])
    if k == None:
        error("Variable not declared")
    generate_code(None, "CRVL", k['scope'], k['offset'], None)
    generate_code(None, "IMPR", None, None, None)

    variable()
    while lookahead("COMMA"):
        expect_token("COMMA")

        k = get_st(actual[2])
        if k == None:
            error("Variable not declared")
        generate_code(None, "CRVL", k['scope'], k['offset'], None)
        generate_code(None, "IMPR", None, None, None)

        variable()
    expect_token("RP")


def structured_statement():
    if lookahead("BEGIN"):
        compound_statement()
    elif lookahead("IF"):
        if_statement()
    elif lookahead("WHILE"):
        while_statement()
    else:
        error("Expected BEGIN, IF or WHILE")


def if_statement():
    expect_token("IF")
    l1 = next_label()
    expression()
    generate_code(None, "DSVF", l1, None, None)
    expect_token("THEN")
    statement()
    if lookahead("ELSE"):
        l2 = next_label()
        generate_code(None, "DSVS", l2, None, None)
        generate_code(l1, "NADA", None, None, None)
        expect_token("ELSE")
        statement()
        generate_code(l2, "NADA", None, None, None)
    else:
        generate_code(l1, "NADA", None, None, None)

def while_statement():
    exp = next_label()
    stop = next_label()

    expect_token("WHILE")
    generate_code(exp, "NADA", None, None, None)
    expression()
    generate_code(None, "DSVF", stop, None, None)
    expect_token("DO")
    statement()
    generate_code(None, "DSVS", exp, None, None)
    generate_code(stop, "NADA", None, None, None)


def expression():
    simple_expression()
    if multi_lookahead(["EQUAL", "NE", "LT", "GT", "LE", "GE", "OR", "AND"]):
        la = None
        if lookahead("LT"):
            la = "LT"
        elif lookahead("GT"):
            la = "GT"
        elif lookahead("LE"):
            la = "LE"
        elif lookahead("GE"):
            la = "GE"
        elif lookahead("EQUAL"):
            la = "EQUAL"
        elif lookahead("AND"):
            la = "AND"
        elif lookahead("OR"):
            la = "OR"
        else:
            error("Unrecognized relational operator")

        relational_operator()
        simple_expression()

        if la == "LT":
            generate_code(None, "CMME", None, None, None)
        elif la == "GT":
            generate_code(None, "CMMA", None, None, None)
        elif la == "LE":
            generate_code(None, "CMEG", None, None, None)
        elif la == "GE":
            generate_code(None, "CMAG", None, None, None)
        elif la == "AND":
            generate_code(None, "CONJ", None, None, None)
        elif la == "OR":
            generate_code(None, "DISJ", None, None, None)
        elif la == "EQUAL":
            generate_code(None, "CMIG", None, None, None)


def simple_expression():
    sign()
    t1 = term()
    la = None
    while multi_lookahead(["PLUS", "MINUS"]):
        if lookahead("PLUS"):
            la = 'PLUS'
            t = 'integer'
        elif lookahead("MINUS"):
            la = 'MINUS'
            t = 'integer'
        else:
            error("UNEXPECTED operator")

        adding_operator()
        t2 = term()

        if la == "PLUS":
            generate_code(None, 'SOMA', None, None, None)
        elif la == "MINUS":
            generate_code(None, 'SUBT', None, None, None)

        if t1 != t or t2 != t:
            print("t:", t, ", t1:", t1, ", t2: ", t2, "\n")
            error("Operation with different data typess")


def term():
    t1 = factor()
    la = None
    while multi_lookahead(["TIMES", "DIV"]):
        if lookahead("TIMES"):
            la = 'TIMES'
            t = 'integer'
        elif lookahead("DIV"):
            la = 'DIV'
            t = 'integer'
        else:
            error("UNEXPECTED operator")
        multiplying_operator()
        t2 = factor()

        if la == "TIMES":
            generate_code(None, 'MULTI', None, None, None)
        elif la == "DIV":
            generate_code(None, 'DIVI', None, None, None)

        if t1 != t or t2 != t:
            error("Operation with different data types")

    return t1


def factor():
    t = None
    if lookahead("IDENTIFIER"):
        k = get_st(actual[2])
        if k == None:
            error("Variable not declared")

        if k['category'] == 'VARS':
            generate_code(None, "CRVL", k['scope'], k['offset'], None)
            t = k['type']
        else:
            error("unrecognized identifier type")

        variable()

    elif lookahead("NUM"):
        generate_code(None, "CRCT", actual[2], None, None)
        t = 'integer'
        constant()
    elif lookahead("LP"):
        expect_token("LP")
        expression()
        expect_token("RP")
    elif lookahead("NOT"):
        # TODO: Check if factor is boolean
        generate_code(None, "NEGA", None, None, None)
        expect_token("NOT")
    else:
        error("Expected IDENTIFIER, NUM, LP, or NOT")

    return t


def relational_operator():
    if consume_token("EQUAL"):
        return
    elif consume_token("NE"):
        return
    elif consume_token("LT"):
        return
    elif consume_token("GT"):
        return
    elif consume_token("LE"):
        return
    elif consume_token("GE"):
        return
    elif consume_token("OR"):
        return
    elif consume_token("AND"):
        return
    else:
        error("Expected RELATIONAL_OPERATOR")


def sign():
    if consume_token("PLUS"):
        pass
    elif consume_token("MINUS"):
        pass


def adding_operator():
    if consume_token("PLUS"):
        pass
    elif consume_token("MINUS"):
        pass
    else:
        error("Expecting PLUS or MINUS")


def multiplying_operator():
    if consume_token("TIMES"):
        pass
    elif consume_token("DIV"):
        pass
    else:
        error("Expecting TIMES or DIV")


def variable():
    expect_token("IDENTIFIER")
    if lookahead("LB"):
        indexed_variable()
    else:
        pass  # skip entire_variable() since we already consumed the IDENTIFIER to be able to lookahead for LB
        # entire_variable()


def indexed_variable():
    expect_token("LB")
    expression()
    expect_token("RB")


def array_variable():
    entire_variable()


def entire_variable():
    variable_identifier()


def variable_identifier():
    identifier()


def constant():
    if lookahead("NUM"):
        integer_constant()
    elif multi_lookahead(["SINGLE_QUOTE", "DOUBLE_QUOTE"]):
        character_constant()
    elif lookahead("IDENTIFIER"):
        constant_identifier()
    else:
        error("Expected NUM, SINGLE_QUOTE, DOUBLE_QUOTE or IDENTIFIER")


def constant_identifier():
    identifier()


def character_constant():
    if lookahead("SINGLE_QUOTE"):
        expect_token("SINGLE_QUOTE")
        expect_token("IDENTIFIER")
        expect_token("SINGLE_QUOTE")
    elif lookahead("DOUBLE_QUOTE"):
        expect_token("DOUBLE_QUOTE")
        expect_token("IDENTIFIER")
        expect_token("DOUBLE_QUOTE")
    else:
        error("Expected SINGLE_QUOTE or DOUBLE_QUOTE")


def integer_constant():
    expect_token("NUM")


def identifier():
    expect_token("IDENTIFIER")


actual = lexer.next()
program()
print('< OK - Sucesso >')

pp = pprint.PrettyPrinter(indent=8)
pp.pprint(symbol_table)
pp.pprint(generated_code)

render_code()

# Check for correct FIRSTs
