import enigma
import unittest
import enigma_exception


class TestEnigmaMethods(unittest.TestCase):

    def test_incorrect_rotor(self):

        # general setup
        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        static = [9, 1, 1]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = []

        for x in range(0, 3):
            for y in range(9, 11):
                rot[x][0] = y
                with self.assertRaises(enigma_exception.InvalidRotor):
                    self.e = enigma.enigma("M4", rot, ref, plugs)
            # reset rotors to ids 1,2,3
            rot[0][0] = 1
            rot[1][0] = 2
            rot[2][0] = 3

        for x in range(1, 9):
            rot[3][0] = x
            with self.assertRaises(enigma_exception.InvalidRotorFour):
                self.e = enigma.enigma("M4", rot, ref, plugs)

    def test_duplicate_rotor(self):

        # general setup
        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        rot = [fast, middle, slow]
        ref = "UKW-B_THIN"
        plugs = []

        rot[0][0] = 1
        rot[1][0] = 1
        rot[2][0] = 3

        with self.assertRaises(enigma_exception.DuplicateRotor):
            self.e = enigma.enigma("M4", rot, ref, plugs)

        rot[0][0] = 1
        rot[1][0] = 2
        rot[2][0] = 2

        with self.assertRaises(enigma_exception.DuplicateRotor):
            self.e = enigma.enigma("M4", rot, ref, plugs)

        rot[0][0] = 3
        rot[1][0] = 2
        rot[2][0] = 3

        with self.assertRaises(enigma_exception.DuplicateRotor):
            self.e = enigma.enigma("M4", rot, ref, plugs)

    def test_incorrect_reflector(self):

        # general setup
        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        rot = [fast, middle, slow]
        plugs = []

        # Enigma I reflector
        options = ["UKW-A", "UKW-B", "UKW-C"]
        for ref in options:
            with self.assertRaises(enigma_exception.InvalidReflector):
                self.e = enigma.enigma("M4", rot, ref, plugs)

    # used for all encrtion tests
    plaintext = ("LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELITSEDD"
                 "OEIUSMODTEMPORINCIDIDUNTUTLABOREETDOLOREMAGNAALIQUAUTE"
                 "NIMADMINIMVENIAMQUISNOSTRUDEXERCITATIONULLAMCOLABORISN"
                 "ISIUTALIQUIPEXEACOMMODOCONSEQUATDUISAUTEIRUREDOLORINRE"
                 "PREHENDERITINVOLUPTATEVELITESSECILLUMDOLOREEUFUGIATNUL"
                 "LAPARIATUREXCEPTEURSINTOCCAECATCUPIDATATNONPROIDENTSUN"
                 "TINCULPAQUIOFFICIADESERUNTMOLLITANIMIDESTLABORUM")

    plaintext = ("LOREMIPSUMDOLORSITAMETCONSECTETURADIPISCINGELITSEDD"
                 "OEIUSMODTEMPORINCIDIDUNTUTLABOREETDOLOREMAGNAALIQUAUTE"
                 "NIMADMINIMVENIAMQUISNOSTRUDEXERCITATIONULLAMCOLABORISN"
                 "ISIUTALIQUIPEXEACOMMODOCONSEQUATDUISAUTEIRUREDOLORINRE"
                 "PREHENDERITINVOLUPTATEVELITESSECILLUMDOLOREEUFUGIATNUL"
                 "LAPARIATUREXCEPTEURSINTOCCAECATCUPIDATATNONPROIDENTSUN"
                 "TINCULPAQUIOFFICIADESERUNTMOLLITANIMIDESTLABORUM")

    def test_encrypt_basic(self):
        # test case 1 (base test)

        crossRef = ("ILFDFARUBDONVISRUKOZQMNDIYCOUHRLAWBRMPYLAZNYNGRMRMV"
                    "AAJLNSZFHSYBBKFODPCHQPHSWOQZCJFKXNBAZJNPZHZBGOMNXOPPXX"
                    "EVJWISBPSDPJQBKZXCTHIVUOJJCSOVBSWFZLGSLFDXMWZWSMHAYRJA"
                    "SZSGQDMQRLKAULWOZNGHSRKVXFQLEVXDWHAWZBXVFBISAAQCNNFYJX"
                    "BAWIYKWCEUOCSKMKHEQGAJDONNHVNJTADKKYRYCYITTAGPDUZMKESM"
                    "IJDCHOKQOEJIOXFMKSLNBKCZGAHMMJRSFVSIYQZJGMCNEMLSOUHZAJ"
                    "XDRBOXVJLMNZUQAMQONCFCOKGESAVPJZESHNZBLEEJOAPXRV")

        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        static = [9, 1, 1]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = []
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_with_plugs(self):

        # test case 2 (plugs added)

        crossRef = ("PLFUFNVDXUSNVPSRYAGZXMZUPYBRDHRWKLWYWPYUNZNYNMRMRXO"
                    "KKKNNSZNHSYOCAVOWPNRZWHSJOXJCJFAQNYKZJNIZPZCOFMRXHTEQQ"
                    "EOJFVSJIAUIJXNKZXEVHPVDOJCLSFVCUDFRLFSLLUQZWVWSTUKYAJK"
                    "YZOEXZMTPOOADYWJTNGHSIARQFXLHKZUZOQWTBQVDCASKIXBNNUYJQ"
                    "VKWPYANBEVOWSAMAORXJKJUONGHVNJTLOAAORRBYPTTKSIDDEBAETM"
                    "PLYDHWKXPEJNUQEMAILNBABZWTEMOYRDKEOTOXCJGMBLEMBOODHZXJ"
                    "QARBLQEIFEDZDXHHCIVBFBOKGESKVITZHSVNWHLEEJCPIQEV")

        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        static = [9, 1, 1]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_start_positions(self):

        # test case 3 (psuedo random start positions)

        crossRef = ("MEYJZTOQPGIHEZIODBVKCPAGUMMQSYXCFTRWKUCDLGHYFFCINOO"
                    "IHVTONWSVJCODFEBDTHWOVVWHPEPZCAURGURZYCLAHMTQEQYJFMVBA"
                    "USFHVXYEUPUURQUGTGCZRTIYBYEXKTYHXVBURKFEHYIBERJUNEMJCH"
                    "XFOLHKGJTQWYRQKGBFRACHZFFARUGJXIAVSPHXXBFWGJSNMJNCZPUY"
                    "IVTMVYQUVPMMCZKCSASSXLGUOBLIEPSDAMCGFWTKGGOOWGYTKBULQY"
                    "QDZCGEPITTYQDDBGNTSVFEVMANWDNHWQXKFBYLGLDXPLTLPKPJHCXI"
                    "LLVKDHMVXOEXKJYPFKJOKHUHUZVXKKPALYDQCLZBXEVMTFDJ")

        fast = [1, 4, 1]
        middle = [2, 19, 1]
        slow = [3, 13, 1]
        static = [9, 17, 1]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_ring_settings(self):

        # test case 4 (psuedo random ring settings)

        crossRef = ("XSVCNOXUDAXRVVIJCOUXIJEJZKJJQURLYVSLTVXRTDPQAPJEURU"
                    "BSHHESLUBHLVABRGFSAQIVIQTGSSEZAOAYYDCAPHDWISIRHMVREOFR"
                    "ODXYMFJKOSQKYBJQZDYPHMMZNXVMPWXUNXREMFWGHUWTRRUBJBBYHF"
                    "CITGZRGXLZLATUNCHKETQRBRNLYFIMZVAIMUPLWGLMFHVYEAWOGFFSX"
                    "FDZVVSIWDONXXUBMJNZMJRVTYJYFZRISVCOTWTGBJJSYTGFSWWDXJFM"
                    "DWYUNNQIUGDJLBWNDGLGSGRUYTRPGWJBQBRNTHMKWKJMOOVFBQLVFKD"
                    "HQZOCXXLIZCZVSBJPZMFWTMNXCWJNWPMOCJSXOFLIVMGC")

        fast = [1, 4, 21]
        middle = [2, 19, 8]
        slow = [3, 13, 2]
        static = [9, 17, 3]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_2extra_rotors(self):

        # test case 5 (use spare rotors)

        crossRef = ("WVXXAMXGWOUIHPGHPUUNSWWGSUXEZLAEXRHEOOKDODHCKHADVIK"
                    "ZQUCDDIQFAYWNHCQMFYKKHJYDSKTESCZSHVRGNJUPCHENGUBYWOVQB"
                    "JMTBZSSEYCQYHPTDWZEJULQUYEHGCWQZBAWCWGYBOCFAVLMLWDMMXQ"
                    "TBFWOZVOWBGJTKRRZRZBMZVGKFMTMORZPXZJJAYVFVODGOEYTYFZNP"
                    "MURDICSWHDQLTTLOENNQPGFONSVSXZRDSPWQBBHDYKPQZUBWPHHBXO"
                    "SNYBPUYHTAPOXPFFDKOWLDZAPETMWINTKCJCUNNVGTYGNBSBPAOEXD"
                    "AFUXGGFLYXDWTRXAKCPTZKBCOGGIIQHBGQZPUYILAQXKWHFX")

        fast = [5, 4, 21]
        middle = [2, 19, 8]
        slow = [4, 13, 2]
        static = [9, 17, 3]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_3extra_rotors(self):

        # test case 6 (use additional Marine rotors)

        crossRef = ("PKGBNSQGPFELOKMXBQDLKLTZRFCLVZVRJSJFGVDETXEAZBDUKXM"
                    "LQBAHCVXOKFNWJEYUYCYBZBCHPFFJECQWROBZHETRSJRWNIHSJHQRW"
                    "PVLXPBPYBPLJZSTAMNFETECAWLTRYJQVLYWFJPTLOOYADCDVYTAYMC"
                    "VMVIRUAATRYBHHQXLHNUDWLIBUPPJPGSWDRCHXOLBKMGOMMSSMBKPM"
                    "WWMRXHZHZKEQADEUYFHQIPHVCBSXRTORJROKNJVAAVQZOYMOOOXEMK"
                    "IJWMSNBMHBPTJVOZBVJCPWEMVIDSMLYBYOMUIKXIOBSWTFQGLLBIGQ"
                    "VDVVKNBHDKBRVLTVGYJMUNBSYEDEHBGAQDVCEAPIYDSPQWDJ")

        fast = [8, 4, 21]
        middle = [7, 19, 8]
        slow = [6, 13, 2]
        static = [9, 17, 3]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_gamma_rotor(self):

        # test case 7 (use gamma rotor)

        crossRef = ("KWBSTXTFVJPBPGXPFKNQOSIDMPWBRPXTNWWZCDCYORYPJCLRLNP"
                    "QNJXGNRIQZQVALVSNVUUFXLEKEKECHSVKMEQGAQGVBPHQJAULFOLLK"
                    "VNIHMVMVKTSSAKHOJYRMRDLYGGRYBIXHROVIOSWPHWJCPAVFQKGZTO"
                    "PIAGXQHFWKHVBRRJZYTYGUWMTTUCDGEKNYQTUIGWNQXUKGXIZQZTTD"
                    "SLDWAQOWKTVMDTBRXOGXZZNBJLYKXLSNROAVLLMHEKKIDSFSPGFQST"
                    "HTYTKMFGMGNLEUHIXDIWLMMZJEYLIPOWRYVNTWMXEQQSHZLQIMLUEEL"
                    "FYSASXSLWYMBRJRBGFZDCXBLLRWRVQOFQENZTVFZHHSWSFV")

        fast = [8, 4, 21]
        middle = [7, 19, 8]
        slow = [6, 13, 2]
        static = [10, 17, 3]
        rot = [fast, middle, slow, static]
        ref = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_reflect_c_thin(self):

        # test case 7 (UWK-C_THIN Reflector)

        crossRef = ("GJBINQJOVXXSVANOFORGCHMBPHVLBOWCZXWAEJVRCYKSSGBQFBA"
                    "SNXQYSGTQSFHWFNYXSCJMSDKSLNOZRSQWKICWEHPOYYRLDPPNFYDMR"
                    "LVENKHJBMVRFQBXSTXNBQNWYNGRBJSYDYCORTJZOHZMHJQHOKWKWEH"
                    "HZKAISKZXFBOFTFFKWHIATMSBOQCSQYENGDIXHKFOCGSZWUZYMWBIY"
                    "AQZSQVOMQBDTDIKGLESYVJZQRANDGXWRRVMRKZXTHEVAONDFXLFMVN"
                    "FORCKRHOYKRSNZDRZTNMFPPJUNRNEKAFFLCMFFZGWBROBUNXSWFMRY"
                    "URMWEHZIUWEEBQQDLHGCIYJZTRIFNCSRBGKEFHAZKEUUKKCJ")

        fast = [5, 4, 21]
        middle = [2, 19, 8]
        slow = [4, 13, 2]
        static = [9, 17, 3]
        rot = [fast, middle, slow, static]
        ref = "UKW-C_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma.enigma("M4", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma.enigma("M4", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_compatability_beta(self):

        fast = [1, 4, 21]
        middle = [2, 19, 8]
        slow = [3, 13, 2]
        # beta rotor
        static = [9, 1, 1]
        rot_M3 = [fast, middle, slow]
        rot_M4 = [fast, middle, slow, static]
        ref_M3 = "UKW-B"
        ref_M4 = "UKW-B_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e_M3 = enigma.enigma("M3", rot_M3, ref_M3, plugs)
        e_M4 = enigma.enigma("M4", rot_M4, ref_M4, plugs)
        ciphertext_M3 = ""
        ciphertext_M4 = ""
        for c in self.plaintext:
            ciphertext_M3 = ciphertext_M3 + e_M3.encrypt(c)
            ciphertext_M4 = ciphertext_M4 + e_M4.encrypt(c)

        # check for proper encryption compatabiltiy
        self.assertEqual(ciphertext_M3, ciphertext_M4)

    def test_compatabiltiy_gamma(self):

        fast = [1, 4, 21]
        middle = [2, 19, 8]
        slow = [3, 13, 2]
        # beta rotor
        static = [10, 1, 1]
        rot_M3 = [fast, middle, slow]
        rot_M4 = [fast, middle, slow, static]
        ref_M3 = "UKW-C"
        ref_M4 = "UKW-C_THIN"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e_M3 = enigma.enigma("M3", rot_M3, ref_M3, plugs)
        e_M4 = enigma.enigma("M4", rot_M4, ref_M4, plugs)
        ciphertext_M3 = ""
        ciphertext_M4 = ""
        for c in self.plaintext:
            ciphertext_M3 = ciphertext_M3 + e_M3.encrypt(c)
            ciphertext_M4 = ciphertext_M4 + e_M4.encrypt(c)

        # check for proper encryption compatabiltiy
        self.assertEqual(ciphertext_M3, ciphertext_M4)

    def test_double_step_single_notch(self):

        fast = [1, 17, 1]
        middle = [2, 4, 1]
        slow = [3, 1, 1]
        static = [9, 1, 1]
        plugs = []
        ref = "UKW-B_THIN"
        rot = [fast, middle, slow, static]
        e = enigma.enigma("M4", rot, ref, plugs)
        self.assertEqual("Z", e.encrypt('A'))
        self.assertEqual("U", e.encrypt('B'))

    def test_double_step_dual_notch(self):

        fast = [8, 26, 1]
        middle = [7, 25, 1]
        slow = [6, 24, 1]
        static = [9, 1, 1]
        plugs = []
        ref = "UKW-B_THIN"
        rot = [fast, middle, slow, static]
        e = enigma.enigma("M4", rot, ref, plugs)
        self.assertEqual("G", e.encrypt('A'))
        self.assertEqual("Y", e.encrypt('B'))

        fast = [8, 13, 1]
        middle = [7, 12, 1]
        slow = [6, 11, 1]
        static = [9, 1, 1]
        plugs = []
        ref = "UKW-B_THIN"
        rot = [fast, middle, slow, static]
        e = enigma.enigma("M4", rot, ref, plugs)
        self.assertEqual("G", e.encrypt('A'))
        self.assertEqual("Y", e.encrypt('B'))


if __name__ == '__main__':
    unittest.main()
