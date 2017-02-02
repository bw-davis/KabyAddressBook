from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter.messagebox import *
from AddressBook import *
from tkinter import messagebox
import re
import datetime
from os import system
from platform import system as platform
from DeletePage import *
from StartPage import *
from SearchPage import *
from DisplayContacts import *



class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        
        print("im in PageOne");
        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller;

        new_contact = []

        # Collect first name from user.
        tk.Label(self, text="First name").grid(column=2, row=2, sticky=(W, E))
        first_name = ttk.Entry(self, width=7);
        first_name.insert(INSERT, "");
        first_name.grid(column=2, row=3, sticky=(W, E));
        # new_contact.append(fname);

        # Collect last name from user.
        tk.Label(self, text="Last name").grid(column=3, row=2, sticky=(W, E))
        last_name = ttk.Entry(self, width=7);
        last_name.grid(column=3, row=3, sticky=(W, E));
        # new_contact.append(lname);


        # Collect address from user
        tk.Label(self, text="Address").grid(column=2, row=4, sticky=(W, E))
        addr = ttk.Entry(self, width=7);
        addr.grid(column=2, row=5, sticky=(W, E));
        # new_contact.append(address);

        # new_contact.append(phone);
        tk.Label(self, text="Address2").grid(column=3, row=4, sticky=(W, E))
        address2= ttk.Entry(self, width=25);
        address2.grid(column=3, row=5, sticky=(W, E));

        # Collect city from user7
        tk.Label(self, text="City").grid(column=2, row=6, sticky=(W, E))
        city = ttk.Entry(self, width=7);
        city.grid(column=2, row=7, sticky=(W, E));
        # new_contact.append(zipC);

        # Collect state from user
        tk.Label(self, text="State").grid(column=3, row=6, sticky=(W, E))
        st = ttk.Entry(self, width=25);
        st.grid(column=3, row=7, sticky=(W, E));
        # new_contact.append(state);

        # Collect zip from user
        tk.Label(self, text="Zip Code").grid(column=2, row=8, sticky=(W, E))
        zip_code = ttk.Entry(self, width=25);
        zip_code.grid(column=2, row=9, sticky=(W, E));
        # new_contact.append(zipC);

        # Collect zip from user
        tk.Label(self, text="Phone Number").grid(column=2, row=10, sticky=(W, E))
        phone_number= ttk.Entry(self, width=25);
        phone_number.grid(column=2, row=11, sticky=(W, E));

        # Collect email from user.
        tk.Label(self, text="Email").grid(column=3, row=10, sticky=(W, E))
        em = ttk.Entry(self, width=7);
        em.grid(column=3, row=11, sticky=(W, E));
        # new_contact.append(email);

        # Bind Enter to create customer as well.

        # ttk.Button(self, text="submit", command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(), state.get(), zipC.get(), em.get(), phone.get())).grid(column=2, row=12);
        ttk.Button(self, text="save",
                   command=lambda: self.add_contact(first_name.get(), last_name.get(), addr.get(), address2.get() , city.get(),
                                                    st.get(), zip_code.get(), em.get(), phone_number.get())).grid(column=2,
                                                                                                          row=12);
        ttk.Button(self, text="cancel", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=12);

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5);

    # AddressBookEnetry(FirstName, LastName, Address1, Address2, City, State, Zipcode, Phone)
    def add_contact(self, fname, lname, address1, address2, city, state, zipC, email, phone):
        """
        Verifies that the inputs are correctly formatted (unless the user doesn't care). If so, the contact
        will be added.
        Args:
            fname:
            lname:
            address1:
            address2:
            city:
            state:
            zipC:
            email:
            phone:

        Returns:
            Nothing but the new contact will be saved.
        """

        # Check to make sure we have at least one name (either first or last) and at least one other field

        temp_list = [fname, lname, address1, address2, city, state, zipC, phone];
        #print("\n\ntemp list {}".format(temp_list))
        

        len_list=[len(x) for x in temp_list]
        print("temp list before checks", end=" ");
        print(temp_list);
        if len_list[0]+len_list[1] > 0:
            print("we have a name")

        if sum(len_list[2:])+len(email)>0:
            print("we have another field")


        if not ((len_list[0]+len_list[1] > 0) and (sum(len_list[2:])+len(email)>0)):
            print("we don't have both a name and an additional field")
            showerror("Error","Error: Please enter a name (at least first or last) AND one additional field.\nPlease fix this before saving.")
            return


        

        # Check the phone number
        if len(temp_list[-1])>0: # don't check if we don't get a phone number passed as an arg

            valid_phone_number=self.valid_phone_number(temp_list[-1])

            print("phone number={} is valid: {}".format(temp_list[-1],str(valid_phone_number)));

            if not valid_phone_number:
                try_again=askokcancel("Warning", "Warning: The phone number you entered is not valid\nClick 'OK' to save anyway\nClick 'Cancel' to edit the phone number")
                if not try_again:
                    return

        # Check the ZIP Code
        if len(temp_list[-2])>0: # don't check if we don't get a ZIP Code passed as an arg

            valid_zip = self.valid_zip(temp_list[-2])

            print("zip={} is valid: {}".format(temp_list[-2], str(valid_zip)));

            if not valid_zip:
                try_again = askokcancel("Warning",
                                        "Warning: The Zip Code you entered is not valid\nClick 'OK' to save anyway\nClick 'Cancel' to edit the Zip Code")
                if not try_again:
                    return

        # Check the email
        if len(email)>0: # don't check if we don't get an email passed as an arg
            valid_email = self.valid_email(email)

            print("email={} is valid: {}".format(temp_list[-1], str(valid_email)));

            if not valid_email:
                try_again = askokcancel("Warning",
                                        "Warning: The email address you entered is not valid\nClick 'OK' to save anyway\nClick 'Cancel' to edit the email address")
                if not try_again:
                    return


        # new_contact=AddressBookEntry(fname, lname, address1, address2, city, state, zipC, phone);
        #print(list_with_skips);
        print("temp list after checks", end=" ");
        print(temp_list);
        list_with_skips = [x if not x == "" else "#skip" for x in temp_list]
        new_contact = AddressBookEntry(*list_with_skips, email=email);
        self.controller.book.addEntry(new_contact);
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);
        set_last_book(self.controller.book_name);
        self.controller.book.saveToFile(self.controller.book_name);

    def valid_phone_number(self, number):
        """
        Function to test whether or not a phone number is valid.
        Args:
            number: the phone numbere

        Returns: True iff the number is of the format ###-###-####  OR ###-#### OR ###.###.####  OR ###.#### OR ####### OR ##########
                 False otherwise
        """
        temp = all([x.isdigit() for x in re.split("\.|-", number)])
        if not temp:
            return False
        l = re.split("\.|-", number)

        if len(l) == 1:
            # If they don't use any . or - to separate the numbers
            if (len(l[0]) == 7 or len(l[0]) == 10):
                return True
            else:
                return False

        if len(l) == 2:
            # We could have a 7 digit phone number
            if len(l[0]) == 3 and len(l[1]) == 4:
                return True
            else:
                return False
        elif len(l) == 3:
            # We could have a 10 digit phone number
            if len(l[0]) == 3 and len(l[1]) == 3 and len(l[2]) == 4:
                return True
            else:
                return False
        else:
            return False

    def valid_email(self, email):
        # checking validation of email
        # format:<string><@><string><.><string>
        # good example: clannad93@qq.com
        #              yuboz@cs.uoregon.edu
        return re.match("([0-9A-z]+)([@]+)([0-9A-z]+)([.]+)([0-9A-z]+)", email) != None


    def valid_zip(self, zipcode):
        # checking validation of Zipcode
        # format:<5 digits>
        #       <5 digits><-><4 digits>
        # good example: 97401
        #              97401-1234

        return re.match("([0-9]){5}([-]{1})([0-9]){4}$", zipcode) != None or re.match("([0-9 a-z]){5}$",zipcode) != None

