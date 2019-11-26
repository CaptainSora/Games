class node:
    def __init__(self, nodetype, memory, info, pos):
        """ Nodetypes:
        Transmitter - [0, 0]
        Receiver - [x, y]
        Tranceiver - [x, y]
        """
        self.type = nodetype

        """ Memory:
        Two-element array [x, y]
        x: filled memory
        y: required memory
        """
        self.memory = memory

        """ Info:
        How much info is on the node
        """
        self.info = info

        """ Pos:
        Two-element array [x, y] for position of node
        """
        self.pos = pos
        