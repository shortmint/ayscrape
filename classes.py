class Htmlstack:
    def __init__(self, linklist):
        self.stack = linklist
        self.index = 0
        self.eol = False

    def peek(self, delta=0):
        try:
            return self.stack[self.index + delta]
        except:
            self.eol = True
            pass

    def pop(self, delta=0):
        item = self.peek(delta)
        if item:
            self.index += 1
        return item
