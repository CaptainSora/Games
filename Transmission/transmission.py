class node:
    def __init__(self, nodetype, memory, info, pos):
        """ Nodetypes:
        Transmitter - Ch. 1
        Receiver - Ch. 1
        Tranceiver - Ch. 2
        Broadcast - Ch. 4
        """
        self.type = nodetype

        """ Memory:
        Two-element array [x, y]
        x: filled memory
        y: required memory
        """
        self.memory = memory

        """ Info:
        How much info is currently on the node
        """
        self.info = info

        """ Pos:
        Two-element array [x, y] for position of node
        """
        self.pos = pos
        