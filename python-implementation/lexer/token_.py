class Token:
    def __init__(self, kind, literal, start, end):
        self.kind = kind
        self.literal = literal
        self.start = start # (line, column)
        self.end = end # (line, column)

    def __repr__(self):
        string = f'{self.kind}'
        if self.literal is not None:
            string += f':{self.literal}'
        return string
