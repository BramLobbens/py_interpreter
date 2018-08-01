class Token:
    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value
        
    def __repr__(self):
        return f'Token({self.type_!r}, {self.value!r})'

