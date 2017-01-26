
from AddressBookEntry import *


"""
AddressBook defined as a container class for AddressBookEntry's. 

Behind-the-scenes data structure is an array
"""
class AddressBook():
    """
    Initializer for AddressBook.

    Instance varaibles:
        entries: array, to be filled with AddressBookEntry objects
    """
    def __init__(self):
        self.entries = []

    """
    Returns the entry at 'index', without removing it

    Args:
        index: int, index of entry to retrieve
    Returns:
        AddressBookEntry, entry at that index
    """
    def getEntry(self, index):
        return self.entries[index]

    """
    Removes AddressBookEntry at 'index'

    Args:
        index: int, index of entry to be removed
    """
    def removeEntry(self, index):
        self.entries.pop(index)

    """
    Adds AddressBookEntry to the end of the AddressBook

    Args:
        entry: AddressBookEntry, the entry to add
    """
    def addEntry(self, entry):
        self.entries.append(entry)

    """
    Sorting method for AddressBook where sorting is done by name
    Sorting by last name, with ties broken by first name

    O(n + n) == O(n)
    """
    def sortByName(self):
        self.entries.sort(key=lambda x: x.getAttribute("FirstName"))
        self.entries.sort(key=lambda x: x.getAttribute("LastName"))

    """
    Sorting method for AddressBook where sorting is done by zip
    Sort by zip, ties broken by last name, ties broken by first name

    O(n + n + n) == O(n)
    """
    def sortByZipcode(self):
        self.entries.sort(key=lambda x: x.getAttribute("FirstName"))
        self.entries.sort(key=lambda x: x.getAttribute("LastName"))
        self.entries.sort(key=lambda x: x.getAttribute("Zipcode"))

    """
    Fills the AddressBook with entries from a file that uses the .tsv format

    Args:
        fn: str, the filename to import entries from
    """
    def importFromFile(self, fn):
        with open(fn) as f:
            n = f.readline() #toss out leading line
            for line in f:
                line = line.strip().split("\t")
                city    = line[0]
                state   = line[1]
                zipcode = line[2]
                addr1   = line[3]
                addr2   = line[4]
                ln      = line[5]
                fn      = line[6]
                phone   = line[7]
                
                entry = AddressBookEntry(fn, ln, addr1, addr2, city, state, zipcode, phone)
                self.addEntry(entry)
        
    """
    Writes the contents of the AddressBook to a file, using .tsv format

    Args:
        fn: str, filename to write address book to
    """
    def exportToFile(self, fn):
        f = open(fn, "w")
        f.write("CITY\tSTATE\tZIP\tdelivery\tSecond\tLastName\tFirstName\tPhone\n")

        for entry in self:
            f.write(entry.getTSVFormat() + "\n")
        f.close()

    """
    Iterator for AddressBook defined as an iterator over the AddressBookEntry list
    """
    def __iter__(self):
        return self.entries.__iter__()

