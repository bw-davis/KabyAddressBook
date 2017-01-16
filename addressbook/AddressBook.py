
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
    Fills the AddressBook with entries from a file

    TODO: File format not specified, currently works with example format

    Args:
        fn: str, the filename to import entries from
    """
    def importFromFile(self, fn):
        with open(fn) as f:
            n = int(f.readline())
            for i in range(n):
                l1 = f.readline().strip()
                l2 = f.readline().strip()
                l3 = f.readline().strip()
                l4 = f.readline().strip()

                fn, ln    = l1.split()
                addr      = l2
                zipcode   = l3.split()[-1]
                citystate = " ".join(l3.split()[:-1])
                email     = l4
                
                entry = AddressBookEntry(fn, ln, addr, citystate, zipcode, email)
                self.addEntry(entry)
        
    """
    Writes the contents of the AddressBook to a file

    TODO: File format not specified, currently works with example format

    Args:
        fn: str, filename to write address book to
    """
    def exportToFile(self, fn):
        f = open(fn, "w")
        f.write(str(len(self.entries)) + "\n")
        
        for entry in self.entries:
            f.write(str(entry) + "\n")
        f.close()

    """
    Iterator for AddressBook defined as an iterator over the AddressBookEntry list
    """
    def __iter__(self):
        return self.entries.__iter__()

