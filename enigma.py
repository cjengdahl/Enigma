import configparser
import rotor
import reflect
import plugboard

config = configparser.ConfigParser(interpolation=configparser.
                                   ExtendedInterpolation())


class enigma:
    """Enigma Machine"""

    def __init__(self, model, rot, ref, plugs):
        """Assembly of Enigma Machine

        Arguments:

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
            a = rotor.rotor(rot[r][0], rot[r][1], rot[r][2])
            self.__rotors.append(a)

        # instantiate reflector
        self.__reflect = reflect.reflect(ref)

        # instantiate plugboard
        self.__plugboard = plugboard.plugboard(10)
        self.add_many_plugs(plugs)

    def add_plug(self, plug):
        """add specified plug, if not already present

        Arguments:

        - plug: string of 2 characters

        Side Effects:

        - plug added to plugboard
        """

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

    def swap_rotor(self, newRotor, oldRotor):
        """change one rotor for another

        Arguments:

        - newRotor: string containing rotor ID

        - oldRotor: string containgin rotor ID
        """

        for r in self.__rotors:
            if self.__rotors[r].rotorId == oldRotor:
                self.__rotors[r].rotorId = newRotor
                break

    def swap_reflect(self, newReflect):
        """change refelctor for another

        Arguments:

        - newReflect: string containing reflector ID

        """

        self.__rf.reflectorId = newReflect

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

        # M4 has a four rotor
        if(self.__model == 'M4'):
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


# fast = [1, 1, 1]
# middle = [2, 1, 1]
# slow = [3, 1, 1]
# group  = 4
# count = 0
# rot = [fast, middle, slow]
# ref = "UKW-B"
# rotors = []
# # plugs = ["AB", "CD", "EF", "GH", "IJ"]
# plugs = []
# e = enigma("ENIGMAI", rot, ref, plugs)
# name = "VVQIRDXPGVHOANLBVJHDUUATKLJKZAIDGJZFKYJGTCEBAFALUACFIWWXUQDDQUIDDHUIBVZRMYFHJFJZRCQGKNWKYWFUGDNQDNZTIXGOHSRQXYUMVKARXSXTURWVEAJZNIUTPQRGYVWQWGYAOLGHERIGVUTCDUQDPPXGPKOXUYREFATTXNKZTVEVWKQZMITQVMNDXFHEDLVQEKEUCDQTHIHFXWJZTUYYRQPGQLWXJKVMSTBXUZMQVBUNHYAIIOUXPQPYROHPDBROOROSLRAMAUOTFJSWQDFMOKOOLSPIBXWGWBFJEMDNJECGJLPBYIVAJADSMPSXUCZYCLPNMGHGLPCIRHUUIHBOUMFWECXWUNEBHUNWMBVCLEVLFFKASRZUQDWPFEXDDKFSPCRQTEIETFKZJJGWWTYHIRBLZQSKEBTRAHZNUECLRGAEAMYNBMUQHAOBDGATZRJHMIMEAEAYSCFZZWKBJTNYTPXVMQFHOZXDHAQKIOCQWCEKIPQFSETXPCPUPAQYKHLCEUFCLIPJJRKZSBQFUJLRIXZRCFKYSNPMECEICXLMVGCRXHYSBFAJMTHMURCROOAEYADJZOYFKUNYXPLSLPYHRIFZOWHJKERXYJDQUUTAQPFTMEACXZCVROYSSBBEPHNSIAKTAWOOZAPBUCDMDLQPQCNPHQOQZONNANSCNNBDLJNLCKHPEPOEQVAPYATAMLAQGOQUYFKVUGETUQUEUHEQKXFPACPKJXWKZ"
# result = ""
# for c in name:
#     if count == 0:
#         result = result + " "

#     result = result + e.encrypt(c)
#     count = (count + 1) % group

# print(result)
