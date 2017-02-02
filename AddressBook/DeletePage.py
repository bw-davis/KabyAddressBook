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
from StartPage import *
from SearchPage import *
from PageOne import *
from DisplayContacts import *


contacts = ["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Phone Number", "Email" ];
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"];



class DeletePage(tk.Frame):
    # the function that will be invoked when user click Delete button in delete page
    def __init__(self, parent, controller):
        print("im in DeletePage");
        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller;

        contact_info = Frame(self, background='black');
        contact_info.grid(row=1, column=0, columnspan=8, sticky='w', padx=20, pady=5);
        row = 0;
        column=0;
        current_row=[];
        for c in ["Delete", "FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "Email"]: 
            label = Text(contact_info, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky='nsew', padx=1, pady=1);
            column +=1;
        row +=1;


        if(len(self.controller.book) > 0):
            f=VerticalScrolledFrame(self);
            f.grid(row=2, column=0, columnspan=8, padx=20);
            f.print_delete_contact_page(contacts);
            self.parent.update_idletasks();

        ttk.Button(self, text="Delete/Save", command=lambda: self.delete_confirm()).grid(row=3, column=2, stick='e');
        # ttk.Button(self, text="Cancel", command=).grid(row=3, column=2);
        ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=3,
                                                                                               stick='w');

    def delete_confirm(self):
        # the function that will be evoked when user click Delete button in delete page
        index = 0
        count = 0
        print("donsomething2");
        print(self.controller.status);
        if askokcancel("Delete", "Are you sure to Delete selected Data?"):
            # pop a dialog let user to confirm
            print("yes")
            # if yes, delete contacts
            for i in self.controller.status:
                if i != 0:
                    print("should delete No.")
                    print(index + 1)
                    self.controller.book.removeEntry(index - count);
                    count += 1
                index += 1;

            set_last_book(self.controller.book_name);
            self.controller.book.saveToFile(self.controller.book_name);
            self.controller.refresh_frame(StartPage);
            self.controller.show_frame(StartPage);
            self.controller.delete_status=[]
        else:
            # if user cancels
            print("No")