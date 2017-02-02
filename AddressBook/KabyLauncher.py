from tkinter import *
import tkinter as tk
from DisplayContacts import *
from tkinter import ttk
import tkinter.filedialog
from tkinter.messagebox import *
from AddressBook import *
from tkinter import messagebox
import re
import datetime
from os import system
from platform import system as platform
from PageOne import *
from DeletePage import *
from StartPage import *
from SearchPage import *


contacts = ["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Phone Number", "Email" ];
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"];

#states = []  # record index of the contacts that you want to delete
edited = False;
skip = "#skip"
starttime = datetime.datetime.now()
endtime = datetime.datetime.now()



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

def on_closing(root):
    if(root.dirty):
            if messagebox.askokcancel("Quit", "Want to save unsaved data?"):
                root.destroy();
    else:
        #print("Nothing to save, quiting")
        root.destroy();

def get_last_book():
    with open('last_book.ini') as f:
        lastbook = f.readline().split("=")[1].strip();
    
    return lastbook;


def set_last_book(new_book):
        print("\n\n new book ={}".format(new_book))
        f = open('last_book.ini', "w")
        to_write="last_book={}".format(new_book);
        f.write(to_write);
        print(to_write)

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


if __name__ == "__main__":
    main() 
