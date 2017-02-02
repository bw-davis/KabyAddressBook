
skip = "#skip"

"""
Object representing an entry into AddressBook

Behind-the-scenes structure is of a dictionary (key-value pairs)

Mandatory fields in an AddressBookEntry are currently:
    first name
    last name
    address line 1
    address line 2 (may be empty)
    city
    state
    zipcode
    phone

Optional fields are allowed in the form of keyward arguments
"""
class AddressBookEntry():
    """
    Initializer of the AddressBookEntry that fills the mandatory fields

    If keyword argument 'dictionary' is True, will set all values to 
    the keyword argument 'attrs'. This is used for cases where all
    attributes are known, and in dictionary form already. 

    Args:
        fn:       str, first name
        ln:       str, last name
        addr1:    str, address line 1
        addr2:    str, address line 2
        city:     str, city
        state:    str, state
        zipcode:  str, zipcode
        phone:    str, phone number
        kwargs:   any optional field such as "email=john@gmail.com"
    """
    def __init__(self, fn, ln, addr1, addr2, city, state, zipcode, phone, **kwargs):
        if 'dictionary' in kwargs and kwargs['dictionary'] == True:
            self.attrs = kwargs['attrs']
            return

        attrs = {"FirstName": fn,
                 "LastName": ln,
                 "Address1": addr1,
                 "Address2": addr2,
                 "City": city,
                 "State": state,
                 "Zipcode": zipcode,
                 "Phone": phone}

        for kw in kwargs.keys():
            attrs[kw] = kwargs[kw]
        self.attrs = attrs

    """
    Setter function to set any attribute of an AddressBookEntry

    Args:
        attr: str, the attribute to change. Example: "FirstName"
        prop: str, the property to set the attribute to. Example: "Francis"
    """
    def setAttribute(self, attr, prop):
        self.attrs[attr] = prop

    """
    Getter function to get any attribute of an AddressBookEntry
    If the attribute does not exist, returns None

    Args:
        attr: str, the attribute to get. Example: "Zipcode"
    """
    def getAttribute(self, attr):
        global skip
        if attr in self.attrs:
            return self.attrs[attr]
        else:
            return skip 

    """
    Searches all fields in the AddressBookEntry for string 'n'

    Args:
        n: str, the string to search for
    Returns:
        true, if string found in any field
        false, otherwise
    """
    def searchAttributes(self, n):
        n = n.lower()
        for key in self.attrs:
            if n in self.attrs[key].lower():
                return True
        return False

    """
    Returns the AddressBookEntry formatted for a line in a .tsv format

    Returns:
        str, entry fields formatted for .tsv file
    """
    def getTSVFormat(self):
        return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.attrs["City"],
                                                       self.attrs["State"],
                                                       self.attrs["Zipcode"],
                                                       self.attrs["Address1"],
                                                       self.attrs["Address2"],
                                                       self.attrs["LastName"],
                                                       self.attrs["FirstName"],
                                                       self.attrs["Phone"]).replace("#skip", "")

    """
    Defines the Python built-in function 'str'

    Behavior defined as printing out the address neatly.
    For example, 
    "John Doe
     123 Sunny Lane
     Apt 1
     Portland, MN 04101
     5411234567"
    """
    def __str__(self):
        return "{} {}\n{}\n{}\n{},{} {}\n{}".format(self.attrs["FirstName"],
                                             self.attrs["LastName"],
                                             self.attrs["Address1"],
                                             self.attrs["Address2"],
                                             self.attrs["City"],
                                             self.attrs["State"],
                                             self.attrs["Zipcode"],
                                             self.attrs["Phone"])

