
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
        self.entries.sort(key=lambda x: x.getAttribute("FirstName").lower())
        self.entries.sort(key=lambda x: x.getAttribute("LastName").lower())
        
        while (not self.entries[0].getAttribute("FirstName").isalnum()): #move null fields to the end
            entry = self.entries.pop(0)
            self.entries.append(entry)
        while (not self.entries[0].getAttribute("LastName").isalnum()):
            entry = self.entries.pop(0)
            self.entries.append(entry)

    """
    Sorting method for AddressBook where sorting is done by name
    Sorting by last name, with ties broken by first name

    O(n + n) == O(n)
    """
    def sortByNameArray(self, search_results):
        search_results.sort(key=lambda x: x.getAttribute("FirstName"))
        search_results.sort(key=lambda x: x.getAttribute("LastName"))
        
        while (not search_results[0].getAttribute("FirstName").isalnum()): #move null fields to the end
            entry = search_results.pop(0)
            search_results.append(entry)
        while (not search_results[0].getAttribute("LastName").isalnum()):
            entry = search_results.pop(0)
            search_results.append(entry)
        
    """
    Sorting method for AddressBook where sorting is done by zip
    Sort by zip, ties broken by last name, ties broken by first name

    O(n + n + n) == O(n)
    """
    def sortByZipcode(self):
        self.sortByName()
        self.entries.sort(key=lambda x: x.getAttribute("Zipcode"))

        length = len(self.entries)
        count  = 0
        while (not self.entries[0].getAttribute("Zipcode").isalnum()):
            count += 1
            if count > length: #in case all zipcodes are empty
                break
            entry = self.entries.pop(0)
            self.entries.append(entry)


    """
    Search method for AddressBook
    Case-insensitive search of both first and last names

    Args:
        n: str, the search string

    Returns:
        list, the indices of the matching entries
    """
    def searchByName(self, n):
        results = []
        n = n.lower()
        for i in range(len(self.entries)):
            entry = self.entries[i]
            if n in entry.getAttribute("FirstName").lower() or n in entry.getAttribute("LastName").lower():
                results.append(i)

        return results

    """
    Search method for AddressBook that check all fields of all entries
    
    Args:
        n: str, the search string

    Returns:
        list, the indices of the matching entries
    """
    def searchByAllFields(self, n):
        results = []
        for i in range(len(self.entries)):
            entry = self.entries[i]
            if entry.searchAttributes(n):
                results.append(i)
        
        return results
                

    """
    Fills the AddressBook with entries from a file that uses the .tsv format
    If force is True, checks leading line against the spec

    Args:
        fn: str, the filename to import entries from
        force: bool, optional argument that specifies whether or not the check
                    the leading line of the .tsv file to match the specifications
    Raises:
        Exception if force == False and leading .tsv line does not match spec
        Exception if error occurs during processing of .tsv file
    """
    def importFromFile(self, fn, force=False):
        tsvfmt = "CITY\tSTATE\tZIP\tdelivery\tSecond\tLastName\tFirstName\tPhone\n"
        with open(fn) as f:
            fmt = f.readline() 
            if force == False and fmt != tsvfmt:
                raise Exception("Possible malformed .tsv file. Header line does not match spec")
            try:
                for line in f:
                    line = line.strip() + "\t" * 8 #in case last field is empty
                    line = line.split("\t")  
                    print(line)
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
            except:
                raise Exception("Error processing .tsv file. Malformed .tsv file.")
        
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
    Creates a new, blank file using .tsv format

    Args:
        fn: str, filename to write address book to
    """
    def saveNewFile(self, fn):
        f = open(fn,"w");
        #f.write("CITY\tSTATE\tZIP\tdelivery\tSecond\tLastName\tFirstName\tPhone\n")
        f.close()

    """
    Populates the AddresBook object with entries from the '.kab' format. 

    Args:
        fn: str, filename to bring entries from
    Raises:
        Exception, if a natural exception occurs during processing of file
    """
    def openFromFile(self, fn):
        try:
            with open(fn) as f:
                for line in f:
                    d = eval(line.strip())
                    entry = AddressBookEntry(None, None, None, None, None, None, None, None, dictionary=True, attrs=d)
                    self.addEntry(entry)
        except:
            raise Exception("Error processing .kab file. Malformed file.")


    """
    Writes the contents of the AddressBook in a specialized '.kab' format. 

    The '.kab' format is defined as the string format of the AddressBookEntry 
    attribute dictionary, one per line. That is, if the file is 30 lines long,
    it contains 30 contacts.

    Args:
        fn: str, filename to save the entries to
    """
    def saveToFile(self, fn):
        f = open(fn, "w")
        for entry in self:
            f.write(str(entry.attrs) + "\n")
        f.close()

    """
    Iterator for AddressBook defined as an iterator over the AddressBookEntry list
    """
    def __iter__(self):
        return self.entries.__iter__()

    """
    Overloading method for built-in 'len' function. 
    """
    def __len__(self):
        return len(self.entries)

