from unittest import TestCase
from gift_exchange.exchange_logic import valid_exchange, run_exchange
from gift_exchange.testutils import valid_matching, directory_builder

class TestExchangeLogic(TestCase):

    def test_valid_exchange_empty(self):
        directory_empty = {}
        self.assertFalse(valid_exchange(directory_empty))
    
    def test_valid_exchange_one_single(self):
        directory_one_single = {"Mike" : None}
        self.assertFalse(valid_exchange(directory_one_single))
    
    def test_valid_exchange_one_couple(self):
        directory_one_couple = {"Mike" : "John", "John" : "Mike"}
        self.assertFalse(valid_exchange(directory_one_couple))

    def test_valid_exchange_two_singles(self):
        directory_two_singles = {"Mike" : None, "John" : None}
        self.assertTrue(valid_exchange(directory_two_singles))

    def test_valid_exchange_one_couple_one_single(self):
        directory_one_couple_one_single = {"Mike" : "John", "John" : "Mike", "Sarah" : None}
        self.assertFalse(valid_exchange(directory_one_couple_one_single))

    def test_valid_exchange_three_singles(self):
        directory_three_singles = {"Mike" : None, "John" : None, "Sarah" : None}
        self.assertTrue(valid_exchange(directory_three_singles))

    def test_valid_exchange_two_couples(self):
        directory_two_couples = {"Mike" : "John", "John" : "Mike", "Sarah" : "Joe", "Joe" : "Sarah"}
        self.assertTrue(valid_exchange(directory_two_couples))

    def test_run_exchange_small_input(self):
        directory_two_singles = directory_builder(2, 0)
        matching_two_singles = run_exchange(directory_two_singles)
        directory_two_couples = directory_builder(4, 2)
        matching_two_couples = run_exchange(directory_two_couples)
        directory_one_couple_two_singles = directory_builder(4, 1)
        matching_one_couple_two_singles = run_exchange(directory_one_couple_two_singles)
        self.assertTrue(valid_matching(directory_two_singles, matching_two_singles))
        self.assertTrue(valid_matching(directory_two_couples, matching_two_couples))
        self.assertTrue(valid_matching(directory_one_couple_two_singles, matching_one_couple_two_singles))

    def test_run_exchange_medium_input(self):
        directory_no_couples = directory_builder(200, 0)
        directory_few_couples = directory_builder(200, 10)
        directory_half_couples = directory_builder(200, 50)
        directory_all_couples = directory_builder(200, 100)  
        matching_no_couples = run_exchange(directory_no_couples)
        matching_few_couples = run_exchange(directory_few_couples)
        matching_half_couples = run_exchange(directory_half_couples)
        matching_all_couples = run_exchange(directory_all_couples)
        self.assertTrue(valid_matching(directory_no_couples, matching_no_couples))
        self.assertTrue(valid_matching(directory_few_couples, matching_few_couples))
        self.assertTrue(valid_matching(directory_half_couples, matching_half_couples))
        self.assertTrue(valid_matching(directory_all_couples, matching_all_couples))

    def test_run_exchange_large_input(self):
        directory_no_couples = directory_builder(10000, 0)
        directory_few_couples = directory_builder(10000, 50)
        directory_half_couples = directory_builder(10000, 2500)
        directory_all_couples = directory_builder(10000, 5000)  
        matching_no_couples = run_exchange(directory_no_couples)
        matching_few_couples = run_exchange(directory_few_couples)
        matching_half_couples = run_exchange(directory_half_couples)
        matching_all_couples = run_exchange(directory_all_couples)
        self.assertTrue(valid_matching(directory_no_couples, matching_no_couples))
        self.assertTrue(valid_matching(directory_few_couples, matching_few_couples))
        self.assertTrue(valid_matching(directory_half_couples, matching_half_couples))
        self.assertTrue(valid_matching(directory_all_couples, matching_all_couples))