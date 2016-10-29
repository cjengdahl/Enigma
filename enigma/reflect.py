import configparser
import os


class Reflect:
    """This is the reflector component of an Enigma Machine"""

    config = configparser.ConfigParser(interpolation=configparser.
                                       ExtendedInterpolation())

    def __init__(self, reflectId,):

        # set relative path to config file
        pwd = os.path.dirname(__file__)
        model_config = os.path.join(pwd, 'model.ini')


        self.__reflectId = reflectId
        self.config.read(model_config)
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
        self.__reflectId = reflectId
        return

    @property
    def wiring(self):
        """Return the reflector wiring."""
        return self.__wiring

    def encrypt(self, letter):
        """Pass a chr (as an integer) through the reflector."""
        return ord(self.__wiring[letter]) - 65
