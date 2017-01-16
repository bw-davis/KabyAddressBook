
from AddressBookEntry import *
from AddressBook import *


def main():
    book = AddressBook()
    book.importFromFile("ExampleAddressBook.txt")
    
    entry = AddressBookEntry("John", "Doe", "123 Daywood Drive", "Portland, MN", "04101", "john@gmail.com")
    book.addEntry(entry)

    for entry in book:
        print(entry)

    book.exportToFile("SavedAddressBook.txt")

if __name__ == "__main__":
    main()
