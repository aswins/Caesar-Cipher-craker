import unittest
import os
from caesar import caesar, check, crack # Imported crack

class TestCaesar(unittest.TestCase):

    def setUp(self):
        # Create a dummy dictionary file for testing the check function
        self.test_dict_path = "test_words_for_check.txt"
        with open(self.test_dict_path, "w") as f:
            f.write("apple\nbanana\ncherry\ndate\nelderberry\nfig\ngrape\n")

    def tearDown(self):
        # Clean up the dummy dictionary file
        if os.path.exists(self.test_dict_path):
            os.remove(self.test_dict_path)

    def test_positive_key(self):
        self.assertEqual(caesar("hello", 3), "khoor")

    def test_large_positive_key(self):
        self.assertEqual(caesar("hello", 29), "khoor") # 29 % 26 = 3

    def test_negative_equivalent_key(self):
        self.assertEqual(caesar("b", -1), "a") 
        self.assertEqual(caesar("b", 25), "a") # 25 is equivalent to -1 mod 26

    def test_character_wraparound(self):
        self.assertEqual(caesar("xyz", 3), "abc")

    def test_mixed_case_punctuation_spaces(self):
        self.assertEqual(caesar("Hello, World!", 5), "mjqqt, btwqi!")

    def test_empty_string(self):
        self.assertEqual(caesar("", 10), "")

    def test_notconverted_characters(self):
        self.assertEqual(caesar("hello, world. ()=123", 3), "khoor, zruog. ()=123")

class TestCheckFunction(unittest.TestCase):
    def setUp(self):
        self.dictionary_path = "test_words.txt" # Using the already created one

    # Test case 1: More than half valid words.
    def test_more_than_half_valid_words(self):
        self.assertTrue(check("apple banana unknown", dictionary_path=self.dictionary_path))

    # Test case 2: Less than half valid words.
    def test_less_than_half_valid_words(self):
        self.assertFalse(check("apple unknown_word another_unknown", dictionary_path=self.dictionary_path))

    # Test case 3: Exactly half valid words.
    def test_exactly_half_valid_words(self):
        self.assertFalse(check("apple banana unknown_one unknown_two", dictionary_path=self.dictionary_path))

    # Test case 4: Empty string.
    def test_empty_string(self):
        self.assertFalse(check("", dictionary_path=self.dictionary_path))

    # Test case 5: All words are valid.
    def test_all_words_valid(self):
        self.assertTrue(check("apple banana cherry", dictionary_path=self.dictionary_path))

    # Test case 6: No words are valid.
    def test_no_words_valid(self):
        self.assertFalse(check("unknown_one unknown_two unknown_three", dictionary_path=self.dictionary_path))

    # Test case 7: String with only spaces
    def test_string_with_only_spaces(self):
        self.assertFalse(check("   ", dictionary_path=self.dictionary_path))

    def test_default_dictionary_not_found(self):
        # Temporarily move the default dict if it exists to simulate it not being found
        default_dict_path = '/usr/share/dict/words'
        moved_default_dict_path = '/usr/share/dict/words_moved_for_test'
        default_dict_exists = os.path.exists(default_dict_path)
        
        if default_dict_exists:
            os.rename(default_dict_path, moved_default_dict_path)
        
        try:
            # Expecting check to print an error and return False
            self.assertFalse(check("test"))
        finally:
            if default_dict_exists: # Move it back
                os.rename(moved_default_dict_path, default_dict_path)

    def test_custom_dictionary_not_found(self):
        with self.assertRaises(FileNotFoundError):
            check("test", dictionary_path="non_existent_dict.txt")

class TestCrackFunction(unittest.TestCase):
    def setUp(self):
        self.dictionary_path = "test_words.txt"

    # Test case 1: Successful crack
    def test_successful_crack(self):
        # "apple" encrypted with key 3 is "dssoh"
        # crack returns (encryption_key, plaintext)
        # caesar("apple", 3) -> "dssoh"
        # The key 'i' in crack is the one that produces the plaintext
        # So, if check(caesar(cipher, i)) is true, it returns (i, caesar(cipher,i))
        # Here, caesar("dssoh", 23) -> "apple" (26-3 = 23)
        # No, wait. The crack function iterates 0 to 25.
        # caesar(sample, key)
        # if sample = "apple", key = 3 -> "dssoh"
        # crack("dssoh") will try caesar("dssoh", i)
        # when i = 23, caesar("dssoh", 23) = "apple". check("apple") is true.
        # So it should return (23, "apple")
        # The main function does `26 - k[0]` for the *original* encryption key.
        # The problem description: `crack("dssoh", dictionary_path="test_words.txt")` should return `(3, "apple")`
        # This implies that `k[0]` from `crack` should be the original encryption key.
        # Let's re-read `crack`:
        #   `temp = caesar(sample,i)`
        #   `if check(temp, dictionary_path=dictionary_path): return i,temp`
        # If `sample` is ciphertext "dssoh", `temp` is plaintext.
        # `caesar("dssoh", key_used_for_decryption)` gives "apple".
        # The key used for decryption here is 23. So `i` will be 23.
        # It returns `(23, "apple")`.
        # If the problem statement means "the key that *encrypted* 'apple' to 'dssoh' was 3",
        # then the test should check for (23, "apple").
        # The main() function prints `26 - k[0]` as "Key". So if k[0] is 23, Key = 3. This makes sense.

        # "apple" is in test_words.txt.
        # caesar("apple", 3) = "dssoh"
        expected_plaintext = "apple"
        # The key `i` returned by `crack` is the key that *decrypts* the ciphertext.
        # So, if ciphertext is "dssoh", and plaintext is "apple",
        # caesar("dssoh", i) = "apple". This `i` is 23.
        result = crack("dssoh", dictionary_path=self.dictionary_path)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 23) # Key that decrypts "dssoh" to "apple"
        self.assertEqual(result[1], expected_plaintext)

        # "banana" encrypted with key 5 is "gfsfsf"
        # caesar("banana", 5) = "gfsfsf"
        # crack("gfsfsf") should try caesar("gfsfsf", i)
        # When i = 21 (26-5), caesar("gfsfsf", 21) = "banana"
        result_banana = crack("gfsfsf", dictionary_path=self.dictionary_path)
        self.assertIsNotNone(result_banana)
        self.assertEqual(result_banana[0], 21) # Key that decrypts "gfsfsf" to "banana"
        self.assertEqual(result_banana[1], "banana")


    # Test case 2: Unsuccessful crack
    def test_unsuccessful_crack(self):
        # "qzxp" is unlikely to decrypt to any word in test_words.txt
        self.assertIsNone(crack("qzxp", dictionary_path=self.dictionary_path))
        self.assertIsNone(crack("xyzzyabccba", dictionary_path=self.dictionary_path))

    # Test case 3: Empty string
    def test_empty_string(self):
        self.assertIsNone(crack("", dictionary_path=self.dictionary_path))

    # Test case 4: Crack with a sentence
    def test_successful_crack_sentence(self):
        # "apple banana" encrypted with key 3 is "dssoh edqdqd"
        # caesar("apple banana", 3) -> "dssoh edqdqd"
        # crack should return (23, "apple banana")
        # Note: check function logic is > 50% words must be valid.
        # "apple banana" -> 2 valid words. 2/2 > 0.5. True.
        result = crack("dssoh edqdqd", dictionary_path=self.dictionary_path)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 23)
        self.assertEqual(result[1], "apple banana")

        # "grape fig date" encrypted with key 7 is "nyhwl mpn khal"
        # caesar("grape fig date", 7) -> "nyhwl mpn khal"
        # crack should return (19, "grape fig date") (26-7 = 19)
        result_sentence = crack("nyhwl mpn khal", dictionary_path=self.dictionary_path)
        self.assertIsNotNone(result_sentence)
        self.assertEqual(result_sentence[0], 19)
        self.assertEqual(result_sentence[1], "grape fig date")

    def test_unsuccessful_crack_sentence_one_valid_word_not_enough(self):
        # "apple qzxp" encrypted with key 3 is "dssoh tcau"
        # caesar("apple qzxp", 3) -> "dssoh tcau"
        # crack("dssoh tcau") will try i=23. temp = "apple qzxp".
        # check("apple qzxp") -> 1 valid, 1 invalid. 1/2 not > 0.5. False.
        self.assertIsNone(crack("dssoh tcau", dictionary_path=self.dictionary_path))


if __name__ == '__main__':
    unittest.main()
