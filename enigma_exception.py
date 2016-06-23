class NoSuchPlug(Exception):
    def __init__(self, plug):
        print(plug, "does not exist")
        Exception.__init__(self, (plug + " does not exist"))


class DuplicatePlug(Exception):
    def __init__(self, plug):
        print(plug, "is a duplicate")
        Exception.__init__(self, (plug + " is a duplicate"))


class MaxPlugsReached(Exception):
    def __init__(self):
        print("Cannot add.  Not enough plugs available")
        Exception.__init__(self, "Cannot add.  Not enough plugs available")
