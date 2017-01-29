import sys
import unittest
import resource

sys.path.append('../AddressBook')

from AddressBook import AddressBookEntry
from AddressBook import AddressBook

class TestSelfAddressEntry(unittest.TestCase):
	def setUp(self):
		self.testEntry = AddressBookEntry('Brian', 'Davis', '492', '83rd', 'Springfield', 'OR', '97478', '123456789')
	def tearDown(self):
		del self.testEntry.attrs
		del self.testEntry

	def test_createEntry(self):
		assert self.testEntry.attrs["FirstName"] == "Brian"
		assert self.testEntry.attrs["LastName"] == "Davis"
		assert self.testEntry.attrs["Address1"] == "492"
		assert self.testEntry.attrs["Address2"] == "83rd"
		assert self.testEntry.attrs["City"] == "Springfield"
		assert self.testEntry.attrs["State"] == "OR"
		assert self.testEntry.attrs["Zipcode"] == "97478"
		assert self.testEntry.attrs["Phone"] == "123456789"

	def test_editEntry(self):
		self.testEntry.setAttribute("FirstName", "Frank")
		assert self.testEntry.attrs["FirstName"] == "Frank"
		self.testEntry.setAttribute("LastName", "Franklin")
		assert self.testEntry.attrs["LastName"] == "Franklin"
		self.testEntry.setAttribute("Address1", "82")
		assert self.testEntry.attrs["Address1"] == "82"
		self.testEntry.setAttribute("Address2", "5")
		assert self.testEntry.attrs["Address2"] == "5"
		self.testEntry.setAttribute("City", "Eugene")
		assert self.testEntry.attrs["City"] == "Eugene"
		self.testEntry.setAttribute("State", "California")
		assert self.testEntry.attrs["State"] == "California"
		self.testEntry.setAttribute("Zipcode", "87654")
		assert self.testEntry.attrs["Zipcode"] == "87654"
		self.testEntry.setAttribute("Phone", "321087654")
		assert self.testEntry.attrs["Phone"] == "321087654"

	def test_getAttribute(self):
		assert self.testEntry.getAttribute("FirstName") == "Brian"

class TestSelfAddressBook(unittest.TestCase):
	def setUp(self):
		self.testAddressBook = AddressBook()
		self.testEntry = AddressBookEntry('Brian', 'Davis', '492', '83rd', 'Springfield', 'OR', '97478', '123456789')
	
	def tearDown(self):
		del self.testAddressBook
		del self.testEntry.attrs
		del self.testEntry

	def test_addEntry(self):
		self.testAddressBook.addEntry(self.testEntry)
		assert self.testAddressBook.entries[0].getAttribute("FirstName") == "Brian"
		assert len(self.testAddressBook.entries) == 1

	def test_removeEntry(self):
		self.testAddressBook.addEntry(self.testEntry)
		self.testAddressBook.removeEntry(0)
		assert len(self.testAddressBook.entries) == 0

	def test_getEntry(self):
		self.testAddressBook.addEntry(self.testEntry)
		assert self.testAddressBook.getEntry(0) == self.testEntry
		self.testAddressBook.removeEntry(0)


