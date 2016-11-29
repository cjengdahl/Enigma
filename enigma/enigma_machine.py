import configparser
from enigma import rotor
from enigma import reflect
from enigma import plugboard
from enigma import enigma_exception

config = configparser.ConfigParser(interpolation=configparser.
                                   ExtendedInterpolation())


class EnigmaMachine:
    """Enigma Machine"""

    def __init__(self, model, rot, ref, plugs):
        """Assembly of Enigma Machine

        Arguments:`

        -model: string containing the Enigma Machine war model

        -rot: list of rotor lists each containing a rotor ID, position
        ,and ring setting

        -ref: string containing reflector ID

        plugs:  list of plugs represented as 2 character strings

        """

        # obtain war model
        self.__model = model
        # instantiate rotors
        self.__rotors = []
        for r in range(0, len(rot)):
            a = rotor.Rotor(rot[r][0], rot[r][1], rot[r][2])
            self.__rotor_check(a)
            self.__rotors.append(a)

        # instantiate reflector
        self.__reflector_check(ref)
        self.__reflect = reflect.Reflect(ref)

        # instantiate plugboard
        self.__plugboard = plugboard.Plugboard(10)
        if len(plugs) > 1:
            self.add_many_plugs(plugs)

    def add_many_plugs(self, plugs):
        """add many plugs, if not already present

        Arguments:

        - plugs: list of plugs represented as strings of 2 characters

        Side Effects:

        - plugs added to plugboard
        """

        self.__plugboard.add_all(plugs)

    def remove_plug(self, plug):
        """remove plug if present

        Arguments:

        - plug: string of 2 characters

        Side Effects:

        - plug removed from plugboard
        """

        self.__plugboard.remove_plug(plug)

    def step(self):
        """Increment rotors according to notches"""
        queue = [self.__rotors[0]]

        if self.__rotors[0].is_turnover() or self.__rotors[1].is_turnover():
            """account for double step"""
            queue.append(self.__rotors[1])
        if self.__rotors[1].is_turnover():
            queue.append(self.__rotors[2])

        for item in queue:
            item.step()

    def step_single(self, r):
        """Manually increment a single rotor"""
        self.__rotors[r].step()

    def rev_step_single(self, r):
        """Manually decrement a single rotor"""
        self.__rotors[r].rev_step()

    def encrypt(self, letter):
        """pass a character through the machine"""
        self.step()
        start = ord(letter.upper()) - 65
        stage1 = self.__plugboard.encrypt(start)
        stage2 = self.__rotors[0].encrypt(stage1, 1)
        stage3 = self.__rotors[1].encrypt(stage2, 1)
        stage4 = self.__rotors[2].encrypt(stage3, 1)

        # M4 has a fourth rotor
        if self.__model == 'M4':
            stageX = self.__rotors[3].encrypt(stage4, 1)
            stage5 = self.__reflect.encrypt(stageX)
            stageY = self.__rotors[3].encrypt(stage5, 2)
            stage6 = self.__rotors[2].encrypt(stageY, 2)

        else:
            stage5 = self.__reflect.encrypt(stage4)
            stage6 = self.__rotors[2].encrypt(stage5, 2)

        stage7 = self.__rotors[1].encrypt(stage6, 2)
        stage8 = self.__rotors[0].encrypt(stage7, 2)
        stage9 = self.__plugboard.encrypt(stage8)

        return chr(stage9 + 65)

    def rotor_pos(self, rotor):
        """returns the current position of indicated rotor"""
        if rotor == "r1":
            return self.__rotors[0].position
        if rotor == "r2":
            return self.__rotors[1].position
        if rotor == "r3":
            return self.__rotors[2].position

    def __rotor_check(self, rotor):
        """check for invalid or duplicate rotor"""

        """invalid rotor check"""
        if (self.__model == "ENIGMAI" and
           (rotor.rotorId < 1 or rotor.rotorId > 5)):
            raise enigma_exception.InvalidRotor(self.__model)

        # Relying on rotor list length prevents check after added to list
        elif ((self.__model == "M4") and len(self.__rotors) == 3 and
              (rotor.rotorId < 9 or rotor.rotorId > 10)):

            raise enigma_exception.InvalidRotorFour()

        elif (not (self.__model == "ENIGMAI") and len(self.__rotors) < 3 and
              (rotor.rotorId < 1 or rotor.rotorId > 8)):

            raise enigma_exception.InvalidRotor(self.__model)

        """duplicate rotor check"""
        ids = []
        for r in self.__rotors:
            ids.append(r.rotorId)

        if rotor.rotorId in ids:
            raise enigma_exception.DuplicateRotor(rotor)

    def __reflector_check(self, reflect):
        """check for invalid reflector"""
        if self.__model.upper() == "ENIGMAI" and not(reflect.upper() == "UKW-A" or
                                             reflect.upper() == "UKW-B" or
                                             reflect.upper() == "UKW-C"):

            raise enigma_exception.InvalidReflector(self.__model)

        elif self.__model == "M4" and not(reflect.upper() == "UKW-B_THIN" or
                                          reflect.upper() == "UKW-C_THIN"):
            raise enigma_exception.InvalidReflector(self.__model)

        elif (not (self.__model.upper() == "ENIGMAI" or self.__model == "M4") and
              not (reflect.upper() == "UKW-B" or reflect.upper() == "UKW-C")):

            raise enigma_exception.InvalidReflector(self.__model)
