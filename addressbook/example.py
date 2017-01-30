"""
Small example file of how to use AddressBook and AddressBookEntry
"""

from AddressBookEntry import *
from AddressBook import *


def main():
    book = AddressBook()
    book.importFromFile("SavedAddressBook2.tsv")

    contact = AddressBookEntry("John", "Doe", "190 Sunny Lane", "", "Portville", "MI", "01404", "5411234567", email="a@a")
    book.addEntry(contact)

    #book.sortByName()
    book.sortByZipcode()

    print("The email: " + contact.getAttribute("Email"))

    for entry in book:
        #print(entry)
        print(entry.getAttribute("email"))

    #searchIndex = book.searchByName("Al")
    #print(searchIndex)

    #book.exportToFile("SavedAddressBook2.tsv")

if __name__ == "__main__":
    main()
