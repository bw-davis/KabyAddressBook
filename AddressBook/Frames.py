"""
This module containes the KabyAddrapp class, when this class is executed a KabyAddrapp instance is created and
the last edited address book.
"""

from pathlib import Path
from tkinter import *
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter.messagebox import *
from AddressBook import *
from tkinter import messagebox
import re
import datetime
import os
from platform import system as platform
#import Frames
from DisplayContacts import *


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
        #self.withdraw();
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


        title_name=self.book_name.split("/");
        app_name=title_name[len(title_name)-1]

        self.title(app_name);
        self.search_contacts=[];
        self.dirty=False;
        self.checkit=[];

        self.frames = {};

        #for F in (StartPage, PageOne):
        starttime = datetime.datetime.now()
       

        endtime = datetime.datetime.now()
        print (endtime - starttime)

        print("StartPage initialize time")


       # for F in (PageOne, DeletePage, StartPage):
        frame = StartPage(self.container, self);
        self.frames[StartPage] = frame;
        frame.grid(row=0, column=0, sticky="nsew");

        starttime = datetime.datetime.now()
        self.show_frame(StartPage);
        self.container.update_idletasks();



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

    def refresh_PageOne(self):
        if self.frames[PageOne] is not None:
            self.frames[PageOne].destroy();
        frame = PageOne(self.controller, self);
        self.frames[PageOne]=frame;
        frame.grid(row=0, column=0, sticky="nsew");

        #if self.frames[cont] is not None:
           #self.frames[cont].destroy()
        #frame = cont(self.container, self)
        #self.frames[cont]=frame;
        #frame .grid(row=0, column=0, sticky="nsew");

    def refresh_frame(self, F):
        print("\n\n\nself.frames={}".format(self.frames));
        print("\n\n\nself.container={}".format(self.container));
        frame = F(self.container, self);
        self.frames[F] = frame;
        frame.grid(row=0, column=0, sticky="nsew");

    def add_contact(contact):
        self.contacts.append(contact)




"""
Class used to display the results of a search on the 
"""
class SearchResultPage(tk.Frame):


    """
    Initializing function to create the SearchResultsPage, this method will display all contacts returned from
    the search function. It also draws all buttons, text entry fields and labels on this screen.
    """
    def __init__(self, parent, controller):
        starttime = datetime.datetime.now()

        print("im in StartPage");

        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller; 

        # Sort by meu
        sort_label = ttk.Label(self, text="Sort by:");
        sort_label.grid(row=0, column=6, stick="e");
        var = StringVar(self);
        options = ["Name", "Zip"];
        var.set(options[0]);
        dropdown = ttk.OptionMenu(self, var, options[0], *options, command=lambda cmd, var=var: self.sort(var.get()));
        dropdown.grid(row=0, column=7, sticky="w");

        search_frame=Frame(self);
        search_frame.grid(row=0, column=0, columnspan=3);

        #search menu
        search_label = ttk.Label(search_frame, text="Search");
        search_label.grid(row=0, column=0, sticky='e', padx=10, pady=5);
        search_input = ttk.Entry(search_frame, width=15);
        search_input.grid(row=0, column=1, sticky='w', pady=5);
        search_button = ttk.Button(search_frame, text="Search", command=lambda  : self.serach_page_search(search_input.get()));
        search_button.grid(row=0, column=3, sticky='e', padx=10);


        contact_info = Frame(self, background='black');
        contact_info.grid(row=1, column=0, columnspan=8, sticky='w', padx=75, pady=5);
        row = 0;
        column=0;
        current_row=[];
        for c in contacts: 
            label = Text(contact_info, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky='nsew', padx=1, pady=1);
            column +=1;
        row +=1;

        #print(self.controller.search_contacts);

        #Displays contacts if there is at least 1 contact in address book.
        if(len(self.controller.book) > 0):
            f=VerticalScrolledFrame(self);
            f.grid(row=2, column=0, columnspan=8, padx=75);
            f.print_search_contacts(self.controller.search_contacts);
        self.parent.update_idletasks();


        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print("now im here")



    #########################################################################
                    ### Methods of the search page class ###
    #########################################################################
    """
    Handles when the user selects a sort option from the sort drop down menu

    ----------------------------------------------------------------------------
        arguments: var => 2 choices from the drop down menu;
                            1.) Name: will call AddressBook method to sort the
                                      address book by last name then display sorted
                                      results.
                            2.) Zip: will call AddressBook method to sort the
                                     contacts by zip code with displays being
                                     displayed on the screen.

        returns: None

        side affects: Contacts that were a result of the search function are 
                      displayed in a sorted manner.
    """
    def sort(self, var):
        print("var is {}".format(var));
        if var == "Name":
            print("sorting by name");
            self.controller.book.sortByNameArray(self.controller.search_contacts);
        else:
            print("sorting by zip");

            self.controller.book.sortByZipcodeArray(self.controller.search_contacts);
        self.controller.refresh_frame(SearchResultPage);
        self.controller.show_frame(SearchResultPage);


    """
    Method called when user clicks the search button at the top right of the corner of the app.

    -------------------------------------------------------------------------------------------
        arguments: name => the value gotten from the text field to the left of the search button.

        returns: None

        side affects: Calls the AddressBook class searchByAllFields method, which returns an array
                      of contacts that have at least 1 field that contains the users search string.
                      The search result page is then refreshed and brought into focus with
                      the contacts being passed as an array to the VerticalScrolledFrame
                      print_contact_search method. This displays the search results.

                      If the entered search string(name) is the empty string or returns
                      no matches then the entire address book is displayed again.
    """
    def serach_page_search(self, name):
        print(name);
        results = self.controller.book.searchByAllFields(name);
        self.controller.search_contacts=[];

        if(((len(results)) > 0) and name):
            print(len(results))

            for i in results:
                #print(i);
                #print(self.controller.book.getEntry(i));
                self.controller.search_contacts.append(self.controller.book.getEntry(i));
            
            self.controller.refresh_frame(SearchResultPage);
            print("Im staying on search page")
            print("name = {}".format(name))
            self.controller.show_frame(SearchResultPage)
        else:
            #print("Going home");
            showerror("Error", "No contact matches\nRedisplaying all contacts");
            self.controller.refresh_frame(StartPage)
            self.controller.show_frame(StartPage)




"""
Class that is used to display all the contacts with a check box next to each contect to allow you to select
which contacts you want to delte.
"""
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

        ttk.Button(self, text="Delete", command=lambda: self.delete_confirm()).grid(row=3, column=2, stick='e');
        # ttk.Button(self, text="Cancel", command=).grid(row=3, column=2);
        ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=3,
                                                                                               stick='w');
    
   

    #########################################################################
                    ### Methods of the delete page class ###
    #########################################################################

    """
    Mehtod used to remove the selected contacts from the address book and the display.
    ----------------------------------------------------------------------------------
        arguments: None

        return: None

        side affects: Deletes the selected contacts from the address book, then redraws the
                      start page with the contacts deleted.
    """
    def delete_confirm(self):
        # the function that will be evoked when user click Delete button in delete page
        index = 0
        count = 0
        #rint("donsomething2");
        #print(self.controller.status);
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 

        if askokcancel("Delete", "Are you sure to permanently Delete the selected Data?"):
        #if (True):
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
        avoidsRandomWindow.destroy();




 

"""
Class that represents the initial or home page of the app. This class displays all contacts in the specified
address book. This frame also provides options for the user to edit, add, or delete contacts, to open new 
or existing address books or to import or export a address book to or from, respectively, a tsv file.
"""
class StartPage(tk.Frame):
    """
    Initializing function to create the StartPag , this method will display all contacts in the address book.
    It also draws all buttons, text entry fields and labels on this screen.
    """
    def __init__(self, parent, controller):
        starttime = datetime.datetime.now()

        print("im in StartPage");

        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller; 

        print(self.controller.status)
        menubar = Menu(parent.master);
        parent.master.config(menu=menubar);
        filemenu = Menu(menubar, tearoff=0);
        menubar.add_cascade(label="File", menu=filemenu);
        filemenu.add_command(label="New", command=self.newBook);
        filemenu.add_command(label="Open", command=self.openAddressBook);
        filemenu.add_command(label="Save", command=self.save);
        filemenu.add_command(label="Save as", command=self.saveAs);
        filemenu.add_command(label="Import", command=self.importFile);
        filemenu.add_command(label="Export", command=self.exportFile);
        filemenu.add_separator();
        filemenu.add_command(label="Exit", command=self.exit_app_option);

        # Edit tab on menu bar
        editmenu = Menu(menubar, tearoff=0);
        menubar.add_cascade(label="Edit", menu=editmenu);
        addmenu = Menu(menubar, tearoff=0);
        editmenu.add_command(label="Add", command= self.to_add_contact_page);#lambda: controller.show_frame(controller.refresh_frame(PageOne)));
        editmenu.add_command(label="Delete", command=self.to_delete_page);

        # Sort by meu
        sort_label = ttk.Label(self, text="Sort by:");
        sort_label.grid(row=0, column=6, stick="e");
        var = StringVar(self);
        options = ["Name", "Zip"];
        var.set(options[0]);
        dropdown = ttk.OptionMenu(self, var, options[0], *options, command=lambda cmd, var=var: self.sort(var.get()));
        dropdown.grid(row=0, column=7, sticky="w");

        

        #search menu
        search_frame=Frame(self);
        search_frame.grid(row=0, column=0, columnspan=3);
        search_label = ttk.Label(search_frame, text="Search");
        search_label.grid(row=0, column=0, sticky='e', padx=10, pady=5);
        search_input = ttk.Entry(search_frame, width=15);
        search_input.grid(row=0, column=1, sticky='w', pady=5);
        search_button = ttk.Button(search_frame, text="Search", command=lambda  : self.start_page_search(search_input.get()));
        search_button.grid(row=0, column=3, sticky='e', padx=10);

        contact_info = Frame(self, background='black');
        contact_info.grid(row=1, column=0, columnspan=8, sticky='w', padx=75, pady=5);
        row = 0;
        column=0;
        current_row=[];
        for c in contacts: 
            label = Text(contact_info, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky='nsew', padx=1, pady=1);
            column +=1;
        row +=1;


        
        if(len(self.controller.book) > 0):
            f=VerticalScrolledFrame(self);
            f.grid(row=2, column=0, columnspan=8, padx=75);
            f.print_contacts(contacts);
        self.parent.update_idletasks();


        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print("now im here")




    #########################################################################
                    ### Methods of the Start Page class ###
    #########################################################################

    """
    Handles exiting app when the x is clicked in the top left of the corner.

    ------------------------------------------------------------------------
        arguments: root => the KabyAddrApp to be closed

        returns: None

        side affects: Checks if address book has been modified. If the book
                      has been modified since last save the user is prompted
                      to save the book.

                      (option 1) if the user clicks save the book is saved then closed

                      (option 2) if the user clicks no all changed data is lost and 
                      book is closed.
    """
    def exit_app(self, root):
        #print("\n\nexiting app={}\n\n".format(self.controller.book_name))
        if(root.dirty):
            avoidsRandomWindow = Tk();
            avoidsRandomWindow.withdraw(); 
            if messagebox.askyesno("Save", "Want to save unsaved data?"):
                root.book.saveToFile(root.book_name);
                set_last_book(root.book_name);
                avoidsRandomWindow.destroy();
                root.destroy();
            else:
                avoidsRandomWindow.destroy();
                root.destroy();
        else:
            root.destroy();



    """
    Handles exiting app when the user chooses the exit option under the file tab

    ----------------------------------------------------------------------------
        arguments: root => None

        returns: None

        side affects: Checks if address book has been modified. If the book
                      has been modified since last save the user is prompted
                      to save the book.

                      (option 1) if the user clicks save the book is saved then closed

                      (option 2) if the user clicks no all changed data is lost and 
                      book is closed.
    """
    def exit_app_option(self):
        #print("\n\nexiting app={}\n\n".format(self.controller.book_name))
        if(self.controller.dirty):
            avoidsRandomWindow = Tk();
            avoidsRandomWindow.withdraw(); 
            if messagebox.askokcancel("Quit", "Want to save unsaved data?"):
                self.controller.book.saveToFile(self.controller.book_name);
                set_last_book(self.controller.book_name);
                avoidsRandomWindow.destroy();
                self.controller.destroy();
            else:
                avoidsRandomWindow.destroy();
                self.controller.destroy();
        else:
            self.controller.destroy();



    """
    Handles when the user selects a sort option from the sort drop down menu

    ----------------------------------------------------------------------------
        arguments: var => 2 choices from the drop down menu;
                            1.) Name: will call AddressBook method to sort the
                                      address book by last name then display sorted
                                      results.
                            2.) Zip: will call AddressBook method to sort the
                                     contacts by zip code with displays being
                                     displayed on the screen.

        returns: None

        side affects: All the contacts are displayed in the manner specified by the
                      sort drop down menu.
    """
    def sort(self, var):
        #Sorting method 
        #print("var is {}".format(var));
        if var == "Name":
            #print("sorting by name");
            self.controller.book.sortByName();
        else:
            print("sorting by zip");
            self.controller.book.sortByZipcode();
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);


    """
    Method called when user clicks delete option under edit menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Refreshes then displays the delete page.
    """
    def to_delete_page(self):
        # click delete in menu bar
        #global states
        self.controller.status = []  # record delete index
        print("I cleaned states 7");
        self.controller.refresh_frame(DeletePage);
        print("Im going to the delete page")
        self.controller.show_frame(DeletePage)


    def to_add_contact_page(self):
        self.controller.refresh_frame(PageOne);
        self.controller.show_frame(PageOne);


    """
    Method called when user clicks new option under file menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Opens a pop up window, requests user to enter path
                      and name of the new address book. The user then either;

                      1) Clicks the save button which saves and displays the
                         new and empty address book.

                      2) Clicks cancel, discards all user input information,
                         and closes pop up window.
    """
    def newBook(self):
        print("donothing");
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        FileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".kab")])
        if FileName!="":
            FileName +=".kab"
            self.controller.book.saveNewFile(FileName);
            newApp = KabyAddrapp(FileName);
            newApp.mainloop();
        print(FileName)
        avoidsRandomWindow.destroy()


    """
    Method called when user clicks import option under file menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Opens a pop up window, requests user to enter path
                      and name of the new of the .tsv file they wish to 
                      import. The user then either;

                      1) Clicks open, which will import all information in
                         the .tsv file. Create a new file with same name and
                         path as the .tsv file just change its extension to .kab
                         and create the first save of the address book. The new 
                         address book with imported information is now imported.

                       2) User clicks cancel, closes pop up window and discards all
                          users input

        format: the .tsv file is expected to have the following format.
                CITY<tab>STATE<tab>ZIP<tab>delivery<tab>Second<tab>LastName<tab>FirstName<tab>Phone
                This line is expected to be the first line of the file, if this line does not exist
                or the form is different a pop up will alert the user the format may not be correct
                then ask if the user would still like to import this file.

    """
    def importFile(self):
        # To import a .tsv file
        print("dosomething");
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        importFileName = tkinter.filedialog.askopenfilename()
        avoidsRandomWindow.destroy()
        if importFileName!="":
             fileNameSplit = importFileName.strip().split("/")
             file = fileNameSplit[-1].strip().split(".");
             kabFileName=file[0]+".kab";
             print(fileNameSplit[-1]);
             print("Kab file {}".format(kabFileName));
 
             try:
                 self.controller.book.importFromFile(importFileName);


                 print("im here")
             except:   
                avoidsRandomWindow = Tk();
                avoidsRandomWindow.withdraw();      
                try_again=askokcancel("Warning", "This is not a standard .tsv file,\n do you still want to import that")
                avoidsRandomWindow.destroy()
                if try_again:
                    try:
                        self.book.importFromFile(addrBook,True);

                    except:
                        print("This is an invalid .tsv file")
                        avoidsRandomWindow = Tk();
                        avoidsRandomWindow.withdraw(); 
                        showerror("Error","This is an invalid .tsv file")
                        avoidsRandomWindow.destroy();

                    else:
                         app2 = KabyAddrapp(importFileName, False);
                         app2.protocol("WM_DELETE_WINDOW", lambda: on_closing(app2));
                         app2.mainloop();

             else:
                     app2 = KabyAddrapp(importFileName, False);
                     app2.protocol("WM_DELETE_WINDOW", lambda: on_closing(app2));
                     app2.mainloop();


        


    """
    Method called when user clicks export option under file menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Opens a pop up window, requests user to enter path
                      and name of the corresponding .tsv file they would
                      like their address book exported to. The user can 
                      then;

                      1) Click export which will save the addresses book 
                         in the user specified tsv file.

                      2) Cancel close the pop up window and discard all
                         user input.
    """
    def exportFile(self):
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        exportFileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".tsv")])+".tsv"
        avoidsRandomWindow.destroy()
        self.controller.book.exportToFile(exportFileName);
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        avoidsRandomWindow.destroy()


    """
    Method called when user clicks open option under file menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Opens a pop up window, requests user to select the .kab
                      address book they would like to open. The user either

                      1) Clicks the open button which opens the specified
                         address book in a new window.

                      2) Clicks cancel, discards all user input information,
                         and closes pop up window.
    """
    def openAddressBook(self):
        #to open an existing  .kab file\
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        AddressbookName = tkinter.filedialog.askopenfilename()
        if AddressbookName!="":
            try:
                self.controller.book.openFromFile(AddressbookName);
                #app2 = KabyAddrapp(AddressbookName);
                #app2.protocol("WM_DELETE_WINDOW", lambda: self.exit_app(app2));
                #app2.mainloop();
                print('I tried here')
                #print(AddressbookName)
                avoidsRandomWindow.destroy()
            except:
                    #print("This is an invalid .tsv file")
                    showerror("Error","This is an invalid .kab file")
                    avoidsRandomWindow.destroy()

            else:
                app2 = KabyAddrapp(AddressbookName);
                app2.protocol("WM_DELETE_WINDOW", lambda: self.exit_app(app2));
                app2.mainloop();
                print(AddressbookName)
                #avoidsRandomWindow.destroy()

    """
    Method called when user clicks save option under file menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Saves all changes to the current address book
                       .kab file
    """
    def save(self):
        #Save the all of the editing
        # print("dosomething");
        # print("dosomething");
        #print("\n\nsaving to = {}\n\n".format(self.controller.book_name))
        self.controller.book.saveToFile(self.controller.book_name);
        self.controller.refresh_frame(StartPage)
        self.controller.show_frame(StartPage)



    """
    Method called when user clicks save as option under file menu tab.

    -----------------------------------------------------------------
        arguments: None

        returns: None

        side affects: Opens a pop up window which requests the user
                      to enter the path and name they'd like to save
                      this address book as. Then user either clicks;

                      1) save, which saves the address book
                         in the specified file. OR

                      2) cancel, closes the pop up window and discards 
                         all user input info.
    """
    def saveAs(self):

        # print("dosomething");
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        FileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".kab")])+".kab"
        avoidsRandomWindow.destroy()
        print(FileName)
        set_last_book(self.controller.book_name);
        self.controller.book.saveToFile(FileName);


    """
    Method called when user clicks the search button at the top right of the corner of the app.

    -------------------------------------------------------------------------------------------
        arguments: name => the value gotten from the text field to the left of the search button.

        returns: None

        side affects: Calls the AddressBook class searchByAllFields method, which returns an array
                      of contacts that have at least 1 field that contains the users search string.
                      The search result page is then refreshed and brought into focus with
                      the contacts being passed as an array to the VerticalScrolledFrame
                      print_contact_search method. This displays the search results.

                      If the entered search string(name) is the empty string or returns
                      no matches then the entire address book is displayed again.
    """
    def start_page_search(self, name):
        #searching function on StartPage
        print(name);
        results = self.controller.book.searchByAllFields(name);
        self.controller.search_contacts=[];


        if(((len(results)) > 0) and name):
            print(len(results))

            for i in results:
                self.controller.search_contacts.append(self.controller.book.getEntry(i));
            
            self.controller.refresh_frame(SearchResultPage);
            print("Im going to the search page")
            print("name = {}".format(name))
            self.controller.refresh_frame(SearchResultPage);
            self.controller.show_frame(SearchResultPage)
        else:
            avoidsRandomWindow = Tk();
            avoidsRandomWindow.withdraw(); 
            showerror("Error", "No contact matches\nRedisplaying all contacts");
            avoidsRandomWindow.destroy()
            self.controller.refresh_frame(StartPage);
            self.controller.show_frame(StartPage)


        

"""
The page that dspalys the page with the fields for you to enter the data about a new contact.
"""
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
        #first_name.insert(INSERT, "");
        first_name.grid(column=2, row=3, sticky=(W, E));

        # Collect last name from user.
        tk.Label(self, text="Last name").grid(column=3, row=2, sticky=(W, E))
        last_name = ttk.Entry(self, width=7);
        last_name.grid(column=3, row=3, sticky=(W, E));


        # Collect address from user
        tk.Label(self, text="Address").grid(column=2, row=4, sticky=(W, E))
        addr = ttk.Entry(self, width=7);
        addr.grid(column=2, row=5, sticky=(W, E));

        # new_contact.append(phone);
        tk.Label(self, text="Address2").grid(column=3, row=4, sticky=(W, E))
        address2= ttk.Entry(self, width=25);
        address2.grid(column=3, row=5, sticky=(W, E));

        # Collect city from user7
        tk.Label(self, text="City").grid(column=2, row=6, sticky=(W, E))
        city = ttk.Entry(self, width=7);
        city.grid(column=2, row=7, sticky=(W, E));

        # Collect state from user
        tk.Label(self, text="State").grid(column=3, row=6, sticky=(W, E))
        st = ttk.Entry(self, width=25);
        st.grid(column=3, row=7, sticky=(W, E));

        # Collect zip from user
        tk.Label(self, text="Zip Code").grid(column=2, row=8, sticky=(W, E))
        zip_code = ttk.Entry(self, width=25);
        zip_code.grid(column=2, row=9, sticky=(W, E));

        # Collect zip from user
        tk.Label(self, text="Phone Number").grid(column=2, row=10, sticky=(W, E))
        phone_number= ttk.Entry(self, width=25);
        phone_number.grid(column=2, row=11, sticky=(W, E));

        # Collect email from user.
        tk.Label(self, text="Email").grid(column=3, row=10, sticky=(W, E))
        em = ttk.Entry(self, width=7);
        em.grid(column=3, row=11, sticky=(W, E));

        # Bind Enter to create customer as well.
        # ttk.Button(self, text="submit", command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(), state.get(), zipC.get(), em.get(), phone.get())).grid(column=2, row=12);
        ttk.Button(self, text="Save",
                   command=lambda: self.add_contact(first_name.get(), last_name.get(), addr.get(), address2.get() , city.get(),
                                                    st.get(), zip_code.get(), em.get(), phone_number.get())).grid(column=2,
                                                                                                          row=12);
        ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=12);

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5);

    """
    Method used to get the user entered data from the the fields for a new contact. At least one of the name fileds is required 
    to be filled out, first or last. Then one addiaionl field must be filled in as well from (address1, address2, city, state, 
    email, phone or zipC)
    -------------------------------------------------------------------------------------------
        parameters: fname => first name of the new contact
                    lname => last name of the new contact
                    address1 => first part of the new contacts address 1234 some street
                    address2 => second part of an address such as apt #1
                    city => city for the new contact
                    state => state for the new contact
                    zipC => zip cod efor the new contact
                    email => email for the new contact
                    phoen => phone number for new contact

        return: None

        side affects: Checks users input to see if nemail, phone, and zip are of the. Prompts the user if input
        is not of the expected form and if not enough data has been entered then the contact will not be added.
        After sufficent data has been added then the new contact will be added to the contact book and the home 
        page will be redrawn with the new contact added.
    """
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
            avoidsRandomWindow = Tk();
            avoidsRandomWindow.withdraw(); 
            showerror("Error","Error: Please enter a name (at least first or last) AND one additional field.\nPlease fix this before saving.")
            avoidsRandomWindow.destroy()
            return


        

        # Check the phone number
        if len(temp_list[-1])>0: # don't check if we don't get a phone number passed as an arg

            valid_phone_number=self.valid_phone_number(temp_list[-1])

            print("phone number={} is valid: {}".format(temp_list[-1],str(valid_phone_number)));

            if not valid_phone_number:
                avoidsRandomWindow = Tk();
                avoidsRandomWindow.withdraw(); 
                try_again=askokcancel("Warning", "Warning: The phone number you entered is not valid\nClick 'OK' to save anyway\nClick 'Cancel' to edit the phone number")
                avoidsRandomWindow.destroy()
                if not try_again:
                    return

        # Check the ZIP Code
        if len(temp_list[-2])>0: # don't check if we don't get a ZIP Code passed as an arg

            valid_zip = self.valid_zip(temp_list[-2])

            print("zip={} is valid: {}".format(temp_list[-2], str(valid_zip)));

            if not valid_zip:
                avoidsRandomWindow = Tk();
                avoidsRandomWindow.withdraw(); 
                try_again = askokcancel("Warning",
                                        "Warning: The Zip Code you entered is not valid\nClick 'OK' to save anyway\nClick 'Cancel' to edit the Zip Code")
                avoidsRandomWindow.destroy()
                if not try_again:
                    return

        # Check the email
        if len(email)>0: # don't check if we don't get an email passed as an arg
            valid_email = self.valid_email(email)

            print("email={} is valid: {}".format(temp_list[-1], str(valid_email)));

            if not valid_email:
                avoidsRandomWindow = Tk();
                avoidsRandomWindow.withdraw(); 
                try_again = askokcancel("Warning",
                                        "Warning: The email address you entered is not valid\nClick 'OK' to save anyway\nClick 'Cancel' to edit the email address")

                avoidsRandomWindow.destroy()
                if not try_again:
                    return


        # new_contact=AddressBookEntry(fname, lname, address1, address2, city, state, zipC, phone);
        #print(list_with_skips);
        print("temp list after checks", end=" ");
        print(temp_list);
        list_with_skips = [x if not x == "" else "#skip" for x in temp_list]
        new_contact = AddressBookEntry(*list_with_skips, email=email);
        #messagebox.showinfo("Contact added", "A new contact has been saved to your address book.")
        msg="New contact \n" + fname + " " + lname + "\nhas been saved to address book "+self.controller.book_name;
        avoidsRandomWindow = Tk();
        avoidsRandomWindow.withdraw(); 
        messagebox.showinfo("Contact added", msg) 
        avoidsRandomWindow.destroy()  
        self.controller.book.addEntry(new_contact);
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);
        set_last_book(self.controller.book_name);
        self.controller.book.saveToFile(self.controller.book_name);








    #########################################################################
                    ### Methods of the new contact page class ###
    #########################################################################

    """
    Mehtod used to validate user phone number
    ------------------------------------------------------------------
        paramter: number => number to be validated

        return: boolean => true if the phone number is of valid from, false if not

        side affects: None
    """
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


    """
    Mehtod used to validate user email
    ------------------------------------------------------------------
        paramter: email => email to be validated

        return: boolean => true if the email is of valid from, false otherwise

        side affects: None
    """
    def valid_email(self, email):
        # checking validation of email
        # format:<string><@><string><.><string>
        # good example: clannad93@qq.com
        #              yuboz@cs.uoregon.edu
        return re.match("([0-9A-z]+)([@]+)([0-9A-z]+)([.]+)([0-9A-z]+)", email) != None




    """
    Mehtod used to validate user zip code
    ------------------------------------------------------------------
        paramter: zipcode => zip code to be validated

        return: boolean => true if the zip code is of valid from, false otherwise

        side affects: None
    """
    def valid_zip(self, zipcode):
        # checking validation of Zipcode
        # format:<5 digits>
        #       <5 digits><-><4 digits>
        # good example: 97401
        #              97401-1234

        return re.match("([0-9]){5}([-]{1})([0-9]){4}$", zipcode) != None or re.match("([0-9 a-z]){5}$",zipcode) != None





"""
Function defines how the first app ran in the main loop below will respond to hitting the x in the top right corner of the screen.
----------------------------------------------------------------------------------------------------------------------------------
    paramters: root => KabyAddrapp book instance being manipulated.

    return: None

    side affects: Closes the KabyAddrapp (root) passed to this Functio
"""
def on_closing(root):
    if(root.dirty):
            avoidsRandomWindow = Tk();
            avoidsRandomWindow.withdraw(); 

            if messagebox.askyesno("Save", "Want to save unsaved data?"):
                root.book.saveToFile(root.book_name);
            avoidsRandomWindow.destroy()
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
    default_book = "SavedAddressBook.kab"
    if(not os.path.isfile(default_book)):
        #addressBook.saveNewFile(default_book);
        f = open(default_book, "w");
        f.close();
    try:#Makes sure the ini file has not been deleted
        with open('last_book.ini') as f:
            try:#This makes sure the contents of ini file have not been modified
                f.readline();
                lastbook = f.readline().split("=")[1].strip();
                try:#Makes sure last book is of appropriate type, else defaults 
                    if(lastbook.split(".")[1]!="kab"):
                        lastbook = default_book
                except: 
                    lastbook = default_book
            except:
                lastbook = default_book
    except:
        lastbook = default_book

    if(not os.path.isfile(lastbook)):
        lastbook=default_book;

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
        #print("\n\n new book ={}".format(new_book))
       # f = open(, "r")
        lines=[];
        to_write="last_book={}".format(new_book);
        lines.append('#do no modify this page\n');
        lines.append(to_write);


        with open("last_book.ini", "w") as file:
            for line in lines:
                file.write(line)
        print(to_write)




"""
Function that executes when the KabyLauncer.py file is executed. This creates the first KabyAddrapp instances.
"""
def main():
    #lastbook = get_last_book();


    app = KabyAddrapp();
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


