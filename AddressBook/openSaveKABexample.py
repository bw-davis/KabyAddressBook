"""
Small example file of how to use AddressBook.openFromFile and AddressBook.saveToFile 
"""

from AddressBookEntry import *
from AddressBook import *


def main():
    book = AddressBook()
    book.openFromFile("SavedAddressBook.kab")

    contact = AddressBookEntry("John", "Doe", "190 Sunny Lane", "", "Portville", "MI", "01404", "5411234567")
    book.addEntry(contact)

    book.sortByZipcode()

    book.saveToFile("SavedAddressBook.kab")

if __name__ == "__main__":
    main()
