import sys
import unittest
import resource

sys.path.append('../AddressBook')

from AddressBook import AddressBookEntry
from AddressBook import AddressBook

class TestSelfAddEntry(unittest.TestCase):
	def setUp(self):
		self.testEntry = AddressBookEntry('Brian', 'Davis', '492', '83rd', 'Springfield', 'OR', '97478', '123456789')
	def tearDown(self):
		del self.testEntry.attrs
		del self.testEntry

	def test_createEntry(self):
		#testEntry = AddressBookEntry('Brian', 'Davis', '492', '83rd', 'Springfield', 'OR', '97478', '123456789')
		assert self.testEntry.attrs["FirstName"] == "Brian"
		assert self.testEntry.attrs["LastName"] == "Davis"
		assert self.testEntry.attrs["Address1"] == "492"
		assert self.testEntry.attrs["Address2"] == "83rd"
		assert self.testEntry.attrs["City"] == "Springfield"
		assert self.testEntry.attrs["State"] == "OR"
		assert self.testEntry.attrs["Zipcode"] == "97478"
		assert self.testEntry.attrs["Phone"] == "123456789"

