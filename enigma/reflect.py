import configparser


class Reflect:
    """This is the reflector component of an Enigma Machine"""

    config = configparser.ConfigParser(interpolation=configparser.
                                       ExtendedInterpolation())

    def __init__(self, reflectId,):
        self.__reflectId = reflectId
        self.config.read('model.ini')
        self.__wiring = list(Reflect.config.get('Reflectors', reflectId))

    @property
    def reflectId(self):
        return self.__reflectId

    @reflectId.setter
    def reflectId(self, reflectId):
        try:
            self.__wiring = list(Reflect.config.get('Reflectors', reflectId))
        except configparser.NoOptionError:
            print(reflectId + " is not a valid reflector ID.")
        return
        self.__reflectId = reflectId

    @property
    def wiring(self):
        """Return the refector wiring."""
        return self.__wiring

    def encrypt(self, letter):
        """Pass a chr (as an integer) through the reflector."""
        return ord(self.__wiring[letter]) - 65
