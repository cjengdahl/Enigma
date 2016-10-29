import unittest
from enigma import enigma_machine
from enigma import enigma_exception


class TestEnigmaMethods(unittest.TestCase):

    def test_incorrect_rotor(self):

        # general setup
        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = []

        for r in rot:
            for x in range(6, 11):
                r[0] = x
                with self.assertRaises(enigma_exception.InvalidRotor):
                    self.e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
            # reset rotors to ids 1,2,3
            rot[0][0] = 1
            rot[1][0] = 2
            rot[2][0] = 3

    def test_duplicate_rotor(self):

        # general setup
        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = []

        rot[0][0] = 1
        rot[1][0] = 1
        rot[2][0] = 3

        with self.assertRaises(enigma_exception.DuplicateRotor):
            self.e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        rot[0][0] = 1
        rot[1][0] = 2
        rot[2][0] = 2

        with self.assertRaises(enigma_exception.DuplicateRotor):
            self.e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        rot[0][0] = 3
        rot[1][0] = 2
        rot[2][0] = 3

        with self.assertRaises(enigma_exception.DuplicateRotor):
            self.e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

    def test_incorrect_reflector(self):

        # general setup
        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        rot = [fast, middle, slow]
        plugs = []

        # M4 only reflector
        ref = "UKW-B_thin"
        with self.assertRaises(enigma_exception.InvalidReflector):
            self.e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        # M4 only reflector
        ref = "UKW-C_thin"
        with self.assertRaises(enigma_exception.InvalidReflector):
            self.e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

    # used for all encrtion tests
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
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = []
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_with_plugs(self):

        # test case 2 (plugs added)

        crossRef = ("PLFUFNVDXUSNVPSRYAGZXMZUPYBRDHRWKLWYWPYUNZNYNMRMRXO"
                    "KKKNNSZNHSYOCAVOWPNRZWHSJOXJCJFAQNYKZJNIZPZCOFMRXHTEQQ"
                    "EOJFVSJIAUIJXNKZXEVHPVDOJCLSFVCUDFRLFSLLUQZWVWSTUKYAJKY"
                    "ZOEXZMTPOOADYWJTNGHSIARQFXLHKZUZOQWTBQVDCASKIXBNNUYJQVKW"
                    "PYANBEVOWSAMAORXJKJUONGHVNJTLOAAORRBYPTTKSIDDEBAETMPLYDH"
                    "WKXPEJNUQEMAILNBABZWTEMOYRDKEOTOXCJGMBLEMBOODHZXJQARBLQEI"
                    "FEDZDXHHCIVBFBOKGESKVITZHSVNWHLEEJCPIQEV")

        fast = [1, 1, 1]
        middle = [2, 1, 1]
        slow = [3, 1, 1]
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_start_positions(self):

        # test case 3 (psuedo random start positions)

        crossRef = ("RCLJKRMGRENHTFVDUNYKUVTLHRIVZCXWKWERUODYLITBQJEXUZB"
                    "WQFOXPRAFLJOSPBGQTXQAIZGSEZTYFKRQCGJDGDAIEMEGCWJVLPHFP"
                    "UJZCOHWVYPKZXHYDGFLDOQLNIZHCFBVBESKLGBLRNOFPJFZLNLMGKRR"
                    "CEDKSINLNZWGQAWVIQEJEBALVIJVQJKNGYOELNUOWHDINTBAJOOXHFV"
                    "TIJYMOCRDKVAWKPGJDYTSDIORZBBRBKGDWFQNQSGDTIAMTADYDYMMEG"
                    "GHQGDQTGIIMCMRZFJZCBNOHVZESMYPVBLRQYRQMWGPDFLQLLZVMOJOP"
                    "WCNGKISFTRYEJQLHRXVWQGVWFQPZLCDKQBMBETIVYVIJ")

        fast = [1, 4, 1]
        middle = [2, 19, 1]
        slow = [3, 13, 1]
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_ring_settings(self):

        # test case 4 (psuedo random ring settings)

        crossRef = ("HQDOTZQRZZELCKEPOVXJFJYAHECMJRZTUVAUFGEOKUFIBEHQMUQ"
                    "LSXOIYEEWABZXGDCEALKIZQNVZWXDCQWVVSSNLBSITAXCXHJYVIMHK"
                    "ZGOJMDYXPOHMZBOPJXFWBCHCHDYQLMMICPYAGSFZJBNFNXTETJGGKO"
                    "HMRXMBOJIMKUTWJNTFHYTKGZKYYPYKZCIOBNKLMMGXLPJGECGTSSVK"
                    "TOQRUFSVGWZNCLZMLHLYIGLNBBHOCGIVJPKVRYWSXSCPJIDWUCYQQW"
                    "CIALKYIONOAMDMJROWBQNSMHRRERFXAJHBNVUNEMJXAHQHUJTIBQHX"
                    "RKLLOSZVTBRINGSWXLWPQBFHDFURKSAXJDVWJLHZMFMOCDPP")

        fast = [1, 4, 21]
        middle = [2, 19, 8]
        slow = [3, 13, 2]
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_extra_rotors(self):

        # test case 5 (use spare rotors)

        crossRef = ("VKCTAEOJVXCQCHWRBOHFXZAFCJCPOGACAKFZWJQZADBMQYWODJP"
                    "VAZIMTGTYTUUYQHGMKRSXGEEBPAMAXFGWUJRKPQNYEWXKQSRKPZODI"
                    "MMSEFJXENKBOLNTDCXBTPIAXSFWRZXDDYAVJAIAPPJMAHRZBCNMWDU"
                    "KBAOVSJDZYQLZTNOQZLYWTUSKHXKUQNXUPLCGMGXFXCANPYCTZVEZA"
                    "TKODTFNLUXGUSKPTDOHJOIZPGPMNYORADAEJNTTXRIDZVQDDNXHRAF"
                    "OBYQWQMIIDDEXMYOVYMPYDNZARYWVHWBKVYBJLJGGFALGELBLWKMXR"
                    "SQUGSXFBFFHIMGBOBBZZJUNJZQFFXQSGBINCHOSZCFEKHFID")

        fast = [5, 4, 21]
        middle = [2, 19, 8]
        slow = [4, 13, 2]
        rot = [fast, middle, slow]
        ref = "UKW-B"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_reflect_a(self):

        # test case 6 (UWK-A Reflector)

        crossRef = ("DPIINKGUZUEWNTTEALRDRAVQTZMAXCWDJQOBMFORTYAISZYNXUA"
                    "FZLLWCAYKRPRCZZUXMGXBRXSWLGFYNLCKIKCPINZDKXVWXMXOADMYQ"
                    "BVRVRTYBDBURZMXSPVMGDMJYDTZXFLGKCCXRUMEJZGXHOXPDSSKOED"
                    "EZOAJMCFDKNQBAKKLJPNTOXUBPPWRWMVQQKRNPILOSBKPWPFYMBIWO"
                    "AJYSYDKTCCXEOYTKLGIYBJRNSHBXFPWYKJQRKFMRNWMLTNIHKPFAVB"
                    "BURFCYZXWTZGNXURCJQREPHLTXPUNURNFDDAIXZYWIGYEXJXZXMORZ"
                    "DSMQWAZOMJPZHBRZQZXHCFJKBUVCZCKPFDLJDQBRDSYUSSPP")

        fast = [5, 4, 21]
        middle = [2, 19, 8]
        slow = [4, 13, 2]
        rot = [fast, middle, slow]
        ref = "UKW-A"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_encrypt_reflect_c(self):

        # test case 7 (UWK-C Reflector)

        crossRef = ("OWGYQFYYGQGXAUXUYEDLPPYLYEYVISVWDIASHYJKPSPURENKHAO"
                    "AHJNZJZBDLVFGMKHUGIBGCVNCNISCHVBAGSMEFCSXSSGOHBOPZLPOH"
                    "OFYMLBZRUDEXMSSZLWTXCSTMFIUQSMALDHQFFPFMWVLUKWOFNXUZAF"
                    "FHYVHYZQREVSVWOJXPALBFNJMSGRETXGFBMLBXRDHQXFIKRRLFGTKL"
                    "JAJFSJWKSRWQRJMUFMCGRYNIFWLLVAQQZYNHZGKUUSZVLTQTYVNSYV"
                    "JEJSIWRABHBBMARQPDBJKYCURFGYICPQOFHRTISICWFIADVPTGJZFB"
                    "GZYPIMNRHMXRDETTUXENLAXSCIBQYVXDDUSHRGVNYJQDQZJB")

        fast = [5, 4, 21]
        middle = [2, 19, 8]
        slow = [4, 13, 2]
        rot = [fast, middle, slow]
        ref = "UKW-C"
        plugs = ["AK", "BC", "UD", "PI", "QX"]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        ciphertext = ""
        for c in self.plaintext:
            ciphertext = ciphertext + e.encrypt(c)

        # check for proper encryption
        self.assertEqual(crossRef, ciphertext)

        # restore initial settings
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)

        original = ""
        for c in ciphertext:
            original = original + e.encrypt(c)

        # check for proper decryption
        self.assertEqual(self.plaintext, original)

    def test_double_step(self):

        fast = [1, 17, 1]
        middle = [2, 4, 1]
        slow = [3, 1, 1]
        plugs = []
        ref = "UKW-B"
        rot = [fast, middle, slow]
        e = enigma_machine.EnigmaMachine("ENIGMAI", rot, ref, plugs)
        self.assertEqual("Z", e.encrypt('A'))
        self.assertEqual("U", e.encrypt('B'))

if __name__ == '__main__':
    unittest.main()
