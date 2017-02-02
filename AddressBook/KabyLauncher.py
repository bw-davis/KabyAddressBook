"""
This module containes the KabyAddrapp class, when this class is executed a KabyAddrapp instance is created and
the last edited address book.
"""

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
from Frames import *
from DisplayContacts import *


contacts = ["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Phone Number", "Email" ];
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"];

#states = []  # record index of the contacts that you want to delete
edited = False;
skip = "#skip"
starttime = datetime.datetime.now()
endtime = datetime.datetime.now()


"""
"""
class KabyAddrapp(tk.Tk):
    #Main frame
    def __init__(self, addrBook="SavedAddressBook.kab", kab_format=True, *args, **kwargs):
        
       

        tk.Tk.__init__(self, *args, **kwargs);
        #self.top = tk.Toplevel(self);
        
        self.container = tk.Frame(self);
        self.status=[];
        #self.top = Toplevel(self.container);

        self.container.grid(row=0, ipadx=25, ipady=10);

        self.container.grid_rowconfigure(0, weight=1);
        self.container.grid_columnconfigure(0, weight=1);
        self.book = AddressBook()
        if(kab_format):
            self.book.openFromFile(addrBook);
            self.book_name=addrBook;
        else:

            ##fix here
            self.book.importFromFile(addrBook,True);
            #self.book.importFromFile(addrBook);
            fileNameSplit = addrBook.strip().split("/")
            file = fileNameSplit[-1].strip().split(".");
            kabFileName=file[0]+".kab";
            self.book_name=kabFileName;


        
        self.search_contacts=[];
        self.dirty=False;
        self.checkit=[];

        self.frames = {};

        #for F in (StartPage, PageOne):
        starttime = datetime.datetime.now()
        frame = StartPage(self.container, self);
        self.frames[StartPage] = frame;
        frame.grid(row=0, column=0, sticky="nsew");

        endtime = datetime.datetime.now()
        print (endtime - starttime)

        print("StartPage initialize time")



        starttime = datetime.datetime.now()
        self.show_frame(StartPage);



        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print ("first time")


    def __enter__(self, *args, **kwargs):
        return self;

    def __exit__(self, *args, **kwargs):
        print("exiting")

    def show_frame(self, cont):
        frame = self.frames[cont];
        frame.tkraise();

    def refresh_frame(self, F):
        frame = F(self.container, self);
        self.frames[F] = frame;
        frame.grid(row=0, column=0, sticky="nsew");

    def add_contact(contact):
        self.contacts.append(contact)









"""
Function defines how the first app ran in the main loop below will respond to hitting the x in the top right corner of the screen.
----------------------------------------------------------------------------------------------------------------------------------
    paramters: root => KabyAddrapp book instance being manipulated.

    return: None

    side affects: Closes the KabyAddrapp (root) passed to this Functio
"""
def on_closing(root):
    if(root.dirty):
            if messagebox.askokcancel("Quit", "Want to save unsaved data?"):
                root.destroy();
    else:
        #print("Nothing to save, quiting")
        root.destroy();


"""
When the app is first launched this function will get the location of the last address book opened, if that file no longer exists 
it will attempt to open the example saved address book in the KabyAddressBook/AddressBook file. If this file has been deleted then
the file KabyAddressBook/AddressBook/SavedAddressBook.kab will be recreated.
----------------------------------------------------------------------------------------------------------------------------------
    paramters: None

    return: lastbook, the path to the last address book edited.

    side affects: None
"""
def get_last_book():
    with open('last_book.ini') as f:
        lastbook = f.readline().split("=")[1].strip();
    
    return lastbook;

"""
Function is called when an address book has been edited and exited to set the default address book to be opened the next time
the app runs.
-----------------------------------------------------------------------------------------------------------------------------
    parameter: None

    return: None

    side affects: Changes the value of the lastbook in the inilitizer file for the app to the last edited addressbook.
"""
def set_last_book(new_book):
        print("\n\n new book ={}".format(new_book))
        f = open('last_book.ini', "w")
        to_write="last_book={}".format(new_book);
        f.write(to_write);
        print(to_write)

"""
Function that executes when the KabyLauncer.py file is executed. This creates the first KabyAddrapp instances.
"""
def main():
    lastbook = get_last_book();
    print(lastbook);



    app = KabyAddrapp(lastbook);
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app));
    starttime = datetime.datetime.now()

    app.mainloop();
    #set_last_book(lastbook);
    endtime = datetime.datetime.now()
    print (endtime - starttime)

"""
Executes main function when this file is executed.
"""
if __name__ == "__main__":
    main() 
