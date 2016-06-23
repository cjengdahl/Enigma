import configparser


class rotor:
    '''A single enigma rotor object'''

    config = configparser.ConfigParser(interpolation=configparser.
                                       ExtendedInterpolation())

    def __init__(self, rotorId, position, ringSetting):
        """rotor initialization

        Arguments:
        -rotorId: an integer identifying active rotor from a set

        -position: an integer (1-26) or character (A-Z) identifying
        the starting rotor position

        -ringSetting: an integer (1-26) or character (A-Z) indentifying
        the starting ring setting

        Side effects:


        """
        # get rotor confguration
        self.config.read('model.ini')

        self.__rotorId = rotorId
        self.__position = position - 1
        self.__ringSetting = ringSetting - 1
        self.__offset = None
        self.__notchCount = rotor.config.getint('Rotors', str(rotorId) + "nn")
        self.__window = None

        self.__baseWiring = list(rotor.config.get('Rotors', str(rotorId)))
        self.__wiring = self.__baseWiring
        self.__turnover = list(rotor.config.get('Rotors', str(rotorId) + 'to'))
        self.configure()
        self.count = 0

    @property
    def rotorId(self):
        """return the rotor ID"""
        return self.__rotorId

    @rotorId.setter
    def rotorId(self, rotorId):
        """set rotor ID, effectivly changing it's wiring

        Arguments:
        -rotorID: a integer identifing active rotor from a set

        Side effects:
        -rotorID changed
        -base wiring of rotor set to newly assigned rotor ID
        -rotor offset and wring reconfugred by call to configure() function
        """
        self.__rotorId = rotorId
        self.__baseWiring = list(rotor.config.get('Rotors', str(rotorId)))
        self.__notchCount = rotor.config.getint('Rotors', str(rotorId) + "nn")
        self.__turnover = list(rotor.config.get('Rotors', str(rotorId) + 'to'))
        self.configure()

    @property
    def position(self):
        """return the resting position of the rotor"""
        return self.__position + 1

    @position.setter
    def position(self, position):
        """set the resting position of the rotor

        Arguments:
        -position:  an integer or character identifying rotor position

        Side effects:
        -rotor position changed
        -rotor offset and wiring reconfigured by call to configure() function
        """

        self.__position = position - 1
        self.configure()

    @property
    def ringSetting(self):
        """return the relative position of the ring"""
        return self.__ringSetting + 1

    @ringSetting.setter
    def ringSetting(self, ringSetting):
        """set the relative position of the ring

        Arguments:
        -ringSetting: an integer or character identifying rotor position

        Side effects:
        -ring setting changed
        -rotor offset and wiring reconfigured by call to configure() function
        """

        self.__ringSetting = ringSetting - 1
        self.configure()

    @property
    def turnover(self):
        """return the rotor turnover location(s)"""
        return self.__turnover

    def is_turnover(self):
        turnover = chr((self.__position) + 65)
        return (turnover in self.__turnover)

    @property
    def window(self):
        """return rotor window"""
        return self.__window

    @window.setter
    def window(self):
        """recompute window based on position and ringSetting

        Arguments:
        -none

        Side effects:
        -window changed/updated
        """

        self.__window = (26 - self.__postion + self.__ringSetting) % 26

    def step(self):
        """increment the rotor one position

        Side effects:
        -rotor postion increased by one
        -rotor offset and wiring reconfigured by call to configure() function
        """

        self.__position += 1
        self.__position %= 26
        self.configure()

    def rev_step(self):
        """decrement the rotor one position

        Arguments:
        -None

        Side effects:
        -rotor postion increased by one
        -rotor offset and wiring reconfigred by call to configure() function
        """

        self.__position -= 1
        self.__position %= 26
        self.configure()

    def encrypt(self, letter, traverse):
        """pass a single character through the rotor]

        Arguments:

        -letter: the character (represented an integer 0 - 26) to be encrypted

        -traverse: integer (either 1 or 2) that indicates if the character
        is being pass forward or backwards through the rotor

        Side effects:
        None
        """

        if traverse == 1:
            if self.__rotorId == 1:
                self.count = self.count + 1
            return ((ord(self.__wiring[letter]) - 65) - self.__offset % 26)
        else:
            return self.__wiring.index(chr(((letter +
                                       self.__offset) % 26) + 65))

    def configure(self):
        """establish effective wiring by computing rotor offset
        Arguments:
        -None

        Side effects:
        -offset computed
        -window computed by calling set_window()
        -wiring reconfigured based on offset
        """

        self.__offset = ((26 - self.__ringSetting + self.__position) % 26)
        self.__wiring = list(self.__baseWiring)
        self.__wiring.extend(self.__wiring[0: self.__offset])
        del self.__wiring[0: self.__offset]

    @property
    def offset(self):
        """return the computed rotor offset"""
        return self.__offset

    @property
    def notch_count(self):
        """return the number of notches in rotor"""
        return self.__notchCount

    @property
    def wiring(self):
        """return the wire map of the rotor"""
        return self.__wiring

    def peek(self):
        """return next encrypted character"""
        return self.__wiring[0]
