from token import Token

INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Interpreter:
    def __init__(self, text):
        # user string input, e.g. "3+5"
        self.text = text
        # index of self.text
        self.pos = 0
        # current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyser (scanner, tokeniser)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # if pos past last index -> EOF
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get char at self.pos and decide what token to create
        current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        # compare current token type with he passed token type,
        # if they match then 'eat' the current token and assign
        # the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type_ == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> <Int> + <Int>"""
        self.current_token = self.get_next_token()

        # we expect current token to be a single-digit integer
        left = self.current_token
        self.eat(INTEGER)

        # we expect current token t be a '+' token
        op = self.current_token
        self.eat(PLUS)

        # we expect current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)

        # after the above call self.current_token is set to
        # EOF token

        return left.value + right.value
