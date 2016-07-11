import plugboard
import reflect
import rotor
import unittest
import enigma_exception


class TestPlugboardMethods(unittest.TestCase):

    def setUp(self):
        # Instantiate pluboard with a supply of 10 plugs
        self.p = plugboard.Plugboard(10)

    def test_add(self):

        # add 9 plugs one-by-one
        self.p.add_plug("AB")
        self.p.add_plug("CD")
        self.p.add_plug("EF")
        self.p.add_plug("GH")
        self.p.add_plug("IJ")
        self.p.add_plug("KL")
        self.p.add_plug("MN")
        self.p.add_plug("OP")
        self.p.add_plug("QR")

        # check how many plugs have been added
        self.assertEqual(self.p.available_plugs, 1)

        # add a duplicate
        p1 = "AB"
        with self.assertRaises(enigma_exception.DuplicatePlug):
            self.p.add_plug(p1)

        # add a reverse duplicate
        p2 = "BA"
        with self.assertRaises(enigma_exception.DuplicatePlug):
            self.p.add_plug(p2)

        # top of the plugboard
        p3 = "ST"
        self.p.add_plug(p3)

        # add one to many
        p4 = "YZ"
        with self.assertRaises(enigma_exception.MaxPlugsReached):
            self.p.add_plug(p4)

    def test_add_all(self):

        # add 10 plugs at once
        a = ["KL", "MN", "OP", "QR", "ST", "AB", "CD", "EF", "GH", "IJ"]
        self.p.add_all(a)

        # check how many plugs have been added
        self.assertEqual(self.p.available_plugs, 0)

        # add way too many
        b = ["KL", "MN", "OP", "QR", "ST"]
        with self.assertRaises(enigma_exception.MaxPlugsReached):
            self.p.add_all(b)

    def test_remove(self):

        # add 5 plugs one by one
        self.p.add_plug("AB")
        self.p.add_plug("CD")
        self.p.add_plug("EF")
        self.p.add_plug("GH")
        self.p.add_plug("IJ")

        # remove 5 plugs one by one
        self.p.remove_plug("AB")
        self.p.remove_plug("CD")
        self.p.remove_plug("EF")
        self.p.remove_plug("GH")
        self.p.remove_plug("IJ")
        self.assertEqual(self.p.available_plugs, 10)

        # remove non-existing plug
        with self.assertRaises(enigma_exception.NoSuchPlug):
            self.p.remove_plug("XY")

    def test_clear(self):

        # clear the rest of the plugs
        self.p.clear()
        self.assertEqual(self.p.available_plugs, 10)

    def test_encrypt(self):

        self.p.add_plug("AB")
        self.p.add_plug("YZ")
        # test encrypt
        self.assertEqual(self.p.encrypt(0), 1)
        self.assertEqual(self.p.encrypt(1), 0)
        self.assertEqual(self.p.encrypt(24), 25)
        self.assertEqual(self.p.encrypt(25), 24)


class TestReflectorMethods(unittest.TestCase):

    def test_encrypt(self):

        # check encryption on "UKW-A"
        r = reflect.Reflect('UKW-A')
        ra = list("EJMZALYXVBWFCRQUONTSPIKHGD")
        for x in range(0, 26):
            self.assertEqual(r.encrypt(x), ord(ra[x]) - 65)

        # check encryption on "UKW-B"
        r = reflect.Reflect('UKW-B')
        rb = list("YRUHQSLDPXNGOKMIEBFZCWVJAT")
        for x in range(0, 26):
            self.assertEqual(r.encrypt(x), ord(rb[x]) - 65)

        # check encryption on "UKW-C"
        r = reflect.Reflect('UKW-C')
        rc = list("FVPJIAOYEDRZXWGCTKUQSBNMHL")
        for x in range(0, 26):
            self.assertEqual(r.encrypt(x), ord(rc[x]) - 65)

        # check encryption on "UKW-B-Thin"
        r = reflect.Reflect('UKW-B_thin')
        rbt = list("ENKQAUYWJICOPBLMDXZVFTHRGS")
        for x in range(0, 26):
            self.assertEqual(r.encrypt(x), ord(rbt[x]) - 65)

        # check encryption on "UKW-C-Thin"
        r = reflect.Reflect('UKW-C_thin')
        rct = list("RDOBJNTKVEHMLFCWZAXGYIPSUQ")
        for x in range(0, 26):
            self.assertEqual(r.encrypt(x), ord(rct[x]) - 65)


class TestRotorMethods(unittest.TestCase):

    # create rotor object
    def setUp(self):
        self.r = rotor.Rotor(1, 1, 1)

    def test_notches(self):
        # iterate through all positions of all roters

        # cross check against notch count of rotor
        self.r.ringSetting = 1
        expected = ['Q', 'E', 'V', 'J', 'Z', 'M', 'Z', 'Z', 'M', 'Z', 'M']
        recorded = []
        for x in range(1, 9):
            self.r.rotorId = x
            self.r.configure()
            count = 0
            for y in range(1, 27):
                self.r.position = y
                self.r.configure()
                if self.r.is_turnover():
                    count += 1
                    recorded.append(chr(self.r.position + 64))
            # check proper amount of notches
            self.assertEqual(count, self.r.notch_count)

        # sort lists for comparisons
        expected.sort()
        recorded.sort()

        # check proper turnover values
        self.assertEqual(expected, recorded)

    def test_step(self):
        self.r.rotorId = 1
        self.r.position = 1
        self.r.ringSetting = 1
        self.assertEqual(self.r.position, 1)
        # step forward
        self.r.step()
        self.assertEqual(self.r.position, 2)
        # step forward twice
        self.r.step()
        self.r.step()
        self.assertEqual(self.r.position, 4)
        # step back
        self.r.rev_step()
        self.assertEqual(self.r.position, 3)

    def test_encryption(self):

        # check encryption on rotorId 1
        self.r.rotorId = 1
        r1 = list("EKMFLGDQVZNTOWYHXUSPAIBRCJ")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r1[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 2
        self.r.rotorId = 2
        r2 = list("AJDKSIRUXBLHWTMCQGZNPYFVOE")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r2[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 3
        self.r.rotorId = 3
        r3 = list("BDFHJLCPRTXVZNYEIWGAKMUSQO")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r3[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 4
        self.r.rotorId = 4
        r4 = list("ESOVPZJAYQUIRHXLNFTGKDCMWB")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r4[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 5
        self.r.rotorId = 5
        r5 = list("VZBRGITYUPSDNHLXAWMJQOFECK")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r5[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 6
        self.r.rotorId = 6
        r6 = list("JPGVOUMFYQBENHZRDKASXLICTW")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r6[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 7
        self.r.rotorId = 7
        r7 = list("NZJHGRCXMYSWBOUFAIVLPEKQDT")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r7[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 8
        self.r.rotorId = 8
        r8 = list("FKQHTLXOCBJSPDZRAMEWNIUYGV")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r8[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 9/Beta
        self.r.rotorId = 9
        r9 = list("LEYJVCNIXWPBQMDRTAKZGFUHOS")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r9[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

        # check encryption on rotorId 10/Gamma
        self.r.rotorId = 10
        r10 = list("FSOKANUERHMBTIYCWLQPZXVGJD")
        for x in range(0, 26):
            trav1 = self.r.encrypt(x, 1)
            self.assertEqual(trav1, ord(r10[x]) - 65)
            trav2 = self.r.encrypt(trav1, 2)
            self.assertEqual(x, trav2)

    def test_configure(self):

        # expected with small position and small ring setting
        self.r.rotorId = 1
        self.r.position = 2
        self.r.ringSetting = 5
        self.r.configure()
        self.assertEqual(self.r.offset, 23)
        expected = list("RCJEKMFLGDQVZNTOWYHXUSPAIB")
        self.assertEqual(self.r.wiring, expected)

        # expected with large position and small ring setting
        self.r.rotorId = 1
        self.r.position = 23
        self.r.ringSetting = 8
        self.r.configure()
        self.assertEqual(self.r.offset, 15)
        expected = list("HXUSPAIBRCJEKMFLGDQVZNTOWY")
        self.assertEqual(self.r.wiring, expected)

        # expected with small position and large ring setting
        self.r.rotorId = 1
        self.r.position = 6
        self.r.ringSetting = 25
        self.r.configure()
        self.assertEqual(self.r.offset, 7)
        expected = list("QVZNTOWYHXUSPAIBRCJEKMFLGD")
        self.assertEqual(self.r.wiring, expected)

        # expected with large position and large ring setting
        self.r.rotorId = 1
        self.r.position = 22
        self.r.ringSetting = 20
        self.r.configure()
        self.assertEqual(self.r.offset, 2)
        expected = list("MFLGDQVZNTOWYHXUSPAIBRCJEK")
        self.assertEqual(self.r.wiring, expected)

if __name__ == '__main__':
    unittest.main()
