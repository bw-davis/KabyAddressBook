from tkinter import *
from DisplayContacts import *
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
from PageOne import *
from DeletePage import *
from StartPage import *
from DisplayContacts import *



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
        contact_info.grid(row=1, column=0, columnspan=8, sticky='w', padx=20, pady=5);
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

        print(self.controller.search_contacts);

        
        if(len(self.controller.book) > 0):
            f=VerticalScrolledFrame(self);
            f.grid(row=2, column=0, columnspan=8, padx=20);
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
            self.controller.book.sortByZipcode();
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

        if(((len(results)) > 1) and name):
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
            print("Going home");
            self.controller.show_frame(StartPage)

