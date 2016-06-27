class NoSuchPlug(Exception):
    def __init__(self, plug):
        Exception.__init__(self, (plug + " does not exist"))


class DuplicatePlug(Exception):
    def __init__(self, plug):
                Exception.__init__(self, (plug + " is a duplicate"))


class MaxPlugsReached(Exception):
    def __init__(self):
        Exception.__init__(self, "Cannot add.  Not enough plugs available")


class DuplicateRotor(Exception):
    def __init__(self, rotor):
        Exception.__init__(self, ("Rotor " + str(rotor.rotorId) +
                           " cannot be used more than once"))


class InvalidRotor(Exception):
    def __init__(self, model):
        if model == "EnigmaI":
            Exception.__init__(self, "RotorId must be 1-5")
        elif model == "M4":
            Exception.__init__(self, "RotorId must be 1-8 (Beta or Gamma if fourth rotor)")
        else:
            Exception.__init__(self, "RotorId must be 1-8")


class InvalidRotorFour(Exception):
    def __init__(self):
        Exception.__init__(self, "Rotor 4 must by of Beta or Gamma type")


class InvalidReflector(Exception):
    def __init__(self, model):
        if model == "EnigmaI":
            Exception.__init__(self, "Reflector must be of type: UKW-A, UKW-B, or UKW-C")
        elif model == "M4":
            Exception.__init__(self, "Reflector must be of type: UKW-B Thin, or UKW-C Thin")
        else:
            Exception.__init__(self, "Reflector must be of type: UKW-B, or UKW-C")
