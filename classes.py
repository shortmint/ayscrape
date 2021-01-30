class Htmlstack:
    def __init__(self, linklist):
        self.stack = linklist
        self.index = 0

    def peek(self, delta=0):
        try:
            return self.stack[self.index + delta]
        except:
            return None

    def pop(self, delta=0):
        item = self.peek(delta)
        if item != None:
            self.index += 1
        return item
