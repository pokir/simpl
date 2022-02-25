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

    def add_child(self, children):
        if hasattr(children, '__iter__'):
            for child in children:
                self.children.append(child)
        else:
            self.children.append(children) # only one child

    def __repr__(self):
        string = f'{self.kind}'
        if self.value is not None:
            string += f'<{self.value}>'
        if self.children is not None:
            string += f'{self.children}'

        return string
