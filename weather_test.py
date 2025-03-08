import requests
import unittest
from weatherapp import valid_zip 

blns_url = "https://raw.githubusercontent.com/minimaxir/big-list-of-naughty-strings/master/blns.txt"

def load_blns():
    response = requests.get(blns_url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

class TestValidation(unittest.TestCase):
    
    def test_valid_zip(self):
        self.assertTrue(valid_zip("12345"))
    
    def test_invalid_zip_length(self):
        self.assertFalse(valid_zip("1234")) 
        self.assertFalse(valid_zip("123456"))
    
    def test_invalid_zip_non_numeric(self):
        self.assertFalse(valid_zip("12a45"))
        self.assertFalse(valid_zip("ABCDE"))
        self.assertFalse(valid_zip("12 45")) 
    
    def test_blns(self): # failed for 01000? not sure if i should be making a specific invalidzip = 01000 since it is 5 digit and all numbers
        blns_cases = load_blns()
        for case in blns_cases:
            with self.subTest(case=case):
                self.assertFalse(valid_zip(case))
    
if __name__ == "__main__":
    unittest.main()
