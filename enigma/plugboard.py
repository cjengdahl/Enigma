from enigma import enigma_exception


class Plugboard:
    """This is a the plugboard component of an Enigma Machine"""

    def __init__(self, max_plugs):
        self.__maxPlugs = max_plugs
        self.__plugs = []

    @property
    def plugs(self):
        """Returns list of currently used plugs"""
        return self.__plugs

    @property
    def max_plugs(self):
        """Returns the maximum number of plugs allowed."""
        return self.__maxPlugs

    @property
    def available_plugs(self):
        """Returns the number of plugs left available to use."""
        return self.__maxPlugs - len(self.__plugs)

    def add_plug(self, plug):
        """Add the a specified plug, if not already present."""

        # check if plugs are available
        self.__plugs_available_check(1)

        # check for duplicate
        self.__plug_check(plug)

        # add plug to list
        self.__plugs.append(list(plug))

    def add_all(self, plugs):
        """Add many specified plugs, if not already present."""
        # check if enough plugs are available
        self.__plugs_available_check(len(plugs))

        # check for duplicates
        for p in plugs:
            self.__plug_check(p)

        # add plugs to plugboard
        for p in plugs:
            self.add_plug(p)

    def remove_plug(self, plug):
        """Remove specified plug, if present"""
        if list(plug) in self.__plugs:
            del self.__plugs[self.__plugs.index(list(plug))]
        else:
            raise enigma_exception.NoSuchPlug(plug)

    def clear(self):
        """Remove all plugs."""
        del self.__plugs[:]

    def encrypt(self, start):
        """Pass a chr (represented as an integer through the plugboard."""
        # If the plug exists, swap the letters
        for plug in self.__plugs:
            if ord(plug[0]) - 65 == start:
                return ord(plug[1]) - 65
            elif ord(plug[1]) - 65 == start:
                return ord(plug[0]) - 65

        # Otherwise, return the passed value unchanged
        return start

    def __plug_check(self, plug):
        """Check for duplicate plugs"""
        for_plug = list(plug)
        rev_plug = [for_plug[1], for_plug[0]]

        # check if plug plugs into self
        if for_plug[0] == for_plug[1]:
            raise enigma_exception.DuplicatePlug(plug)

        # check for duplicate sockets are used
        for pair in self.__plugs:
            if for_plug[0] in list(pair) or for_plug[1] in list(pair):
                raise enigma_exception.DuplicatePlug(plug)

    def __plugs_available_check(self, plugCount):
        """Check for plug availability"""
        if plugCount > self.available_plugs:
            raise enigma_exception.MaxPlugsReached()
