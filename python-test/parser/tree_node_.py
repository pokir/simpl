class TreeNode:
    def __init__(self, kind, start, end, value=None, raw=None, children=None):
        # Leave the arguments at None only if the node kind will never use
        # those arguments
        # (put children=[] if it will eventually have children)
        self.kind = kind
        self.start = start # (line, column)
        self.end = end     # (line, column)
        self.value = value
        self.raw = raw
        self.children = children

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        string = f'{self.kind}'
        if self.value is not None:
            string += f'<{self.value}>'
        if self.children is not None:
            string += f'{self.children}'

        string += f'{self.start} to {self.end}'

        return string
