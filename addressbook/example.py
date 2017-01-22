"""
Small example file of how to use AddressBook and AddressBookEntry
"""

from AddressBookEntry import *
from AddressBook import *


def main():
    book = AddressBook()
    book.importFromFile("ExampleAddressBook.tsv")

    for entry in book:
        print(entry)

    contact = AddressBookEntry("John", "Doe", "190 Sunny Lane", "", "Portville", "MI", "01404", "5411234567")
    book.addEntry(contact)

    #book.sortByName()
    book.sortByZipcode()

    book.exportToFile("SavedAddressBook.tsv")

if __name__ == "__main__":
    main()
