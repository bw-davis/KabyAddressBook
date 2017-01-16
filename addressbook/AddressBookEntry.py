

"""
Object representing an entry into AddressBook

Behind-the-scenes structure is of a dictionary (key-value pairs)

Mandatory fields in an AddressBookEntry are currently:
    first name
    last name
    address
    city
    state
    zipcode
    email
"""
class AddressBookEntry():
    """
    Initializer of the AddressBookEntry that fills the mandatory fields

    Args:
        fn: str, first name
        ln: str, last name
        addr: str, address
        cs: str, city and state
        zipcode: str, zipcode
        email: str, email
    """
    def __init__(self, fn, ln, addr, cs, zipcode, email):
        attrs = {"FirstName": fn,
                 "LastName": ln,
                 "Address": addr,
                 "CityState": cs,
                 "Zipcode": zipcode,
                 "Email": email}
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
        if attr in self.attrs:
            return self.attrs[attr]
        else:
            return None

    """
    Defines the Python built-in function 'str'

    Behavior is defined 
    """
    def __str__(self):
        return "{} {}\n{}\n{} {}\n{}".format(self.attrs["FirstName"],
                                             self.attrs["LastName"],
                                             self.attrs["Address"],
                                             self.attrs["CityState"],
                                             self.attrs["Zipcode"],
                                             self.attrs["Email"])

