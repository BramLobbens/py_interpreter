from collections import namedtuple

Token = namedtuple('Token', 'type_ value')
INTEGER, PLUS, MINUS, MULT, DIV, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EOF'

class Interpreter:
    def __init__(self, text):
        # user string input, e.g. "112 - 57"
        self.text = text
        # index of self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        """Advance the 'pos' pointer and set the 'current_char' variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None # end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        """Lexical analyser (scanner, tokeniser)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MULT, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            self.error()

        return Token(EOF, None)

    def eat(self, token_type):
        # compare current token type with he passed token type,
        # if they match then 'eat' the current token and assign
        # the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type_ == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def term(self):
        """return an INTEGER token value"""
        token = self.current_token
        self.eat(INTEGER)
        return token.value

    def expr(self):
        """
        Parser/Interpreter

        expr -> <Int> <Operator> <Int>
        """

        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        result = self.term()
        while self.current_token.type_ in (PLUS, MINUS, MULT, DIV):
            token = self.current_token
            if token.type_ == PLUS:
                self.eat(PLUS)
                result = result + self.term()
            if token.type_ == MINUS:
                self.eat(MINUS)
                result = result - self.term()
            if token.type_ == MULT:
                self.eat(MULT)
                result = result * self.term()
            elif token.type_ == DIV:
                self.eat(DIV)
                try:
                    result = result / self.term()
                except ZeroDivisionError:
                    print('Error: trying to divide by zero.')
                    return

        return result

