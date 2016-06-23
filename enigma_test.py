import plugboard
import reflect
import rotor
import enigma
import unittest
import enigma_exception


class TestPlugboardMethods(unittest.TestCase):

    def test_add(self):

        p = plugboard.plugboard(6)

        # add 5 plugs one-by-one
        p.add_plug("AB")
        p.add_plug("CD")
        p.add_plug("EF")
        p.add_plug("GH")
        p.add_plug("IJ")

        # check how many plugs have been added
        self.assertEqual(p.get_available(), 1)

        # add a duplicate
        p1 = "AB"
        # self.assertRaises(p.add_plug(p1), enigma_exception.DuplicatePlug(p1))
        with self.assertRaises(enigma_exception.DuplicatePlug):
            p.add_plug(p1)

        # add a reverse duplicate
        p2 = "BA"
        # self.assertRaises(p.add_plug(p2), enigma_exception.DuplicatePlug(p2))
        with self.assertRaises(enigma_exception.DuplicatePlug):
            p.add_plug(p2)

        # top of the plugboard
        p3 = "KL"
        p.add_plug(p3)

        # add one to many
        p4 = "YZ"
        # self.assertRaises(p.add_plug(p3), enigma_exception.MaxPlugsReached())
        with self.assertRaises(enigma_exception.MaxPlugsReached):
            p.add_plug(p4)

    def test_add_all(self):

        p = plugboard.plugboard(5)

        # add 5 plugs at once
        a = ["KL", "MN", "OP", "QR", "ST"]
        b = ["AB", "CD", "EF", "GH", "IJ"]
        p.add_all(a)

        # check how many plugs have been added
        self.assertEqual(p.get_available(), 0)

        # add way to many
        with self.assertRaises(enigma_exception.MaxPlugsReached):
            p.add_all(b)

    def test_remove(self):

        p = plugboard.plugboard(10)

        # add 5 plugs one by one
        p.add_plug("AB")
        p.add_plug("CD")
        p.add_plug("EF")
        p.add_plug("GH")
        p.add_plug("IJ")

        # remove 5 plugs one by one
        p.remove_plug("AB")
        p.remove_plug("CD")
        p.remove_plug("EF")
        p.remove_plug("GH")
        p.remove_plug("IJ")
        self.assertEqual(p.get_available(), 10)

        # remove non-existance plug
        with self.assertRaises(enigma_exception.NoSuchPlug):
            p.remove_plug("XY")

    def test_clear(self):

        p = plugboard.plugboard(10)

        # clear the rest of the plugs
        p.clear()
        self.assertEqual(p.get_available(), 10)

    def test_encrypt(self):

        p = plugboard.plugboard(10)
        p.add_plug("AB")
        p.add_plug("YZ")
        # test encrypt
        self.assertEqual(p.encrypt(0), 1)
        self.assertEqual(p.encrypt(1), 0)
        self.assertEqual(p.encrypt(24), 25)
        self.assertEqual(p.encrypt(25), 24)


class TestReflectorMethods(unittest.TestCase):

    def test_wiring(self):
        r = reflect.reflect('UKW-A')

        # expected wiring
        ra = list("EJMZALYXVBWFCRQUONTSPIKHGD")
        rb = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        rc = list("FVPJIAOYEDRZXWGCTKUQSBNMHL")
        rbt = list("ENKQAUYWJICOPBLMDXZVFTHRGS")
        rct = list("RDOBJNTKVEHMLFCWZAXGYIPSUQ")
        self.assertEqual(ra, r.get_wiring())
        r.set_reflectId("UKW-B")
        self.assertEqual(rb, r.get_wiring())
        r.set_reflectId("UKW-C")
        self.assertEqual(rc, r.get_wiring())
        r.set_reflectId("UKW-B_thin")
        self.assertEqual(rbt, r.get_wiring())
        r.set_reflectId("UKW-C_thin")
        self.assertEqual(rct, r.get_wiring())

    def test_encrypt(self):

        # check encryption on a single rotor
        r = reflect.reflect('UKW-A')
        ra = list("EJMZALYXVBWFCRQUONTSPIKHGD")
        for x in range(0, 26):
            self.assertEqual(r.encrypt(x), ord(ra[x]) - 65)


class TestRotorMethods(unittest.TestCase):

    # create rotor object
    def setUp(self):
        self.r = rotor.rotor(1, 1, 1)

    def test_notches(self):
        # iterate through all positions of all roters

        # cross check against notch count of rotor
        self.r.set_ringSetting(1)
        expected = ['Q', 'E', 'V', 'J', 'Z', 'M', 'Z', 'Z', 'M', 'Z', 'M']
        recorded = []
        for x in range(1, 9):
            self.r.set_rotorId(x)
            self.r.configure()
            count = 0
            for y in range(1, 27):
                self.r.set_position(y)
                self.r.configure()
                if self.r.is_turnover():
                    count += 1
                    recorded.append(self.r.peek())
            self.assertEqual(count, self.r.get_notch_count())

        # check proper turnover values
        self.assertEqual(expected, recorded)

    def test_step(self):
        self.r.set_rotorId(1)
        self.r.set_position(1)
        self.r.set_ringSetting(1)
        self.assertEqual(self.r.get_positon(), 1)
        # step forward
        self.r.step()
        self.assertEqual(self.r.get_positon(), 2)
        # step forward twice
        self.r.step()
        self.r.step()
        self.assertEqual(self.r.get_positon(), 4)
        # step back
        self.r.rev_step()
        self.assertEqual(self.r.get_positon(), 3)

    def test_encryption(self):
        # set up rotor
        self.r.set_rotorId(1)
        self.r.set_position(1)
        self.r.set_ringSetting(1)
        self.r.configure()
        # encrypt A/0 expect E/4
        self.assertEqual(self.r.encrypt(0, 1), 4)
        # encrypt Z/25 expect J/9
        self.assertEqual(self.r.encrypt(25, 1), 9)

        # check symmetry of rotor

        # encrypt E/4 expect A/0
        self.assertEqual(self.r.encrypt(4, 2), 0)
        # encrypt J/9 expect Z/25
        self.assertEqual(self.r.encrypt(9, 2), 25)

    def test_configure(self):

        # expected with small position and small ring setting
        self.r.set_rotorId(1)
        self.r.set_position(2)
        self.r.set_ringSetting(5)
        self.r.configure()
        self.assertEqual(self.r.get_offset(), 23)
        expected = list("RCJEKMFLGDQVZNTOWYHXUSPAIB")
        self.assertEqual(self.r.get_wiring(), expected)

        # expected with large position and small ring setting
        self.r.set_rotorId(1)
        self.r.set_position(23)
        self.r.set_ringSetting(8)
        self.r.configure()
        self.assertEqual(self.r.get_offset(), 15)
        expected = list("HXUSPAIBRCJEKMFLGDQVZNTOWY")
        self.assertEqual(self.r.get_wiring(), expected)

        # expected with small position and large ring setting
        self.r.set_rotorId(1)
        self.r.set_position(6)
        self.r.set_ringSetting(25)
        self.r.configure()
        self.assertEqual(self.r.get_offset(), 7)
        expected = list("QVZNTOWYHXUSPAIBRCJEKMFLGD")
        self.assertEqual(self.r.get_wiring(), expected)

        # expected with large position and large ring setting
        self.r.set_rotorId(1)
        self.r.set_position(22)
        self.r.set_ringSetting(20)
        self.r.configure()
        self.assertEqual(self.r.get_offset(), 2)
        expected = list("MFLGDQVZNTOWYHXUSPAIBRCJEK")
        self.assertEqual(self.r.get_wiring(), expected)


class TestEnigmaMethods(unittest.TestCase):

    def __create_enigma():
        r1 = [1, 1, 1]
        r2 = [2, 1, 1]
        r3 = [3, 1, 1]
        rot = [r1, r2, r3]
        plugs = []
        ref = "UKW-B"
        e = enigma("ENIGMAI", rot, ref, plugs)
        return e

    def test_step(self):
        e = self.__create_enigma()

    def test_encrypt(self):
        """ Test three cases of known configuration
        for proper encryption
        """

        # Case 1

        e = self.__create_enigma()

        # T input, - ouput

        # Case 2

        r1 = [1, 1, 1]
        r2 = [2, 1, 1]
        r3 = [3, 1, 1]
        rot = [r1, r2, r3]
        plugs = []
        ref = "UKW-B"
        e = enigma("ENIGMAI", rot, ref, plugs)

        # R input, - ouput

        # Case 3

        r1 = [1, 1, 1]
        r2 = [2, 1, 1]
        r3 = [3, 1, 1]
        rot = [r1, r2, r3]
        plugs = []       
        ref = "UKW-B"
        e = enigma("ENIGMAI", rot, ref, plugs)

        # Y input, - ouput




























if __name__ == '__main__':
    unittest.main()
