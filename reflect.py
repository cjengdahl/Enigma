import configparser


class reflect:
    '''This is the reflector component of an Enigma Machine'''

    config =configparser.ConfigParser(interpolation= configparser.ExtendedInterpolation())

    def __init__(self, reflectId,):
        self.__reflectId = reflectId
        # get reflector confguration
        self.config.read('model.ini')
        self.__wiring = list(reflect.config.get('Reflectors', reflectId))

    def set_reflectId(self, newReflect):
        """Set the reflector ID, effectivly chanigng it's wiring"""
        try:
            self.__wiring = list(reflect.config.get('Reflectors', newReflect))
        except configparser.NoOptionError:
            print(newReflect + " is not a valid reflector ID.")
        return
        self.__reflectId = newReflect

    def get_reflectId(self):
        """Return the reflector ID."""
        return self.__reflectId

    def get_wiring(self):
        """Return the refector wiring."""
        return self.__wiring

    def encrypt(self, letter):
        """Pass a chr (as an integer) through the reflector."""
        return ord(self.__wiring[letter]) - 65
