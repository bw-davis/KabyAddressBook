"""
Small example file of how to use search methods of AddressBook 
"""

from AddressBookEntry import *
from AddressBook import *


def main():
    book = AddressBook()
    book.importFromFile("SavedAddressBook.tsv")

    for entry in book:
        print(entry)

    searchIndex = book.searchByAllFields("OR")
    print(searchIndex)

    #book.exportToFile("SavedAddressBook2.tsv")

if __name__ == "__main__":
    main()
