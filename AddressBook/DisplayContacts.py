"""
This module contains VerticalScrolledFrame with methods to display contacts in 3 different formats
    print_contacts => method used to display all contacts on the start page.

    print_search_contacts => method used to display selected contacts that match the results of a search 
                             in the search page.

    print_delete_contact_page=> method used to display all contacts and the check box to select contacts 
                                to delete

This page also contians methods to edit and delete contacts and display the scroll bar.

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
from KabyLauncher import *

#Array used to display atribute at top of contcts
contacts = ["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Phone Number", "Email" ];
#Array of AddressBookEntry atributes to be displayed
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"];
edited = False;
skip = "#skip"


"""
Classed use to display all contacts in a vertical scroll bar window. It has methods to draw the contacts in 
3 formats, the start page format, the SearchResultPage format, and the DeletePage format.
"""
class VerticalScrolledFrame(tk.Frame):
    """
    Initalizes a scrollable tk window.
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)  
        self.parent=parent          

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas, background='black')
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        """
        track changes to frame inside the canvas.
        """
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)


        """
        track changes to the canvas and frame width and sync them,
        also updating the scrollbar.
        """
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


    """
    Mehtod used to handle delete button click on DeletePage
    ----------------------------------------------------------------------------
        arguments: i=> index of contact in address book to delete

        return: None

        side affects: sefts the status array to 1 at index of each contact to delete
                       this array is used to delete contacts.
    """
    def onPress(self, i):
        self.parent.controller.status[i] = 1;


    """
    Method used to handle if the user clicks the enter button after editing a contact info.
    ---------------------------------------------------------------------------------------
        arguments: row => the row this entry appears on in the displayed table
                   col => colunm the entry appears in
                   entry => the entry to be modified.

        reutrn: None

        side affects: Edits the specified attribute for a contact and redraws this 
                      attribute highlighted in blue.
    """
    def update_contact(self, row, col, entry):
        attr = col_name[col];  # The contact attribute to be replaceed
        contact = self.parent.controller.book.getEntry(row);  # Contact to be modified
        contact_attr = contact.getAttribute(attr);  # The contact attribute to be replaced
        new_contact_data = entry.get("1.0", END).replace('\n','');  # The text that has been entered in the Text widget. The end-1c ignores newline charater
        entry.delete("1.0", END);
        entry.delete("2.0", END);
        entry.insert(INSERT, new_contact_data);
        entry.tag_add("a", "1.0", END);
        entry.tag_configure("a", background="skyblue");
        contact.setAttribute(attr, new_contact_data);
        self.parent.controller.dirty=True;
        

    """
    Method used to check if contact info has been updated after a user clicks out of cell
    -------------------------------------------------------------------------------------
        arguments: r => the row this entry appears on in the displayed table
                   c => colunm the entry appears in
                   entry => the entry to be modified.

        reutrn: None

        side affects: Edits the specified attribute for a contact and redraws this 
                      attribute highlighted in blue.
    """  
    def redraw_entry(self, r, c, entry):
        val=entry.get("1.0", END);
        if(self.parent.controller.checkit):
            last_entry, row, col = self.parent.controller.checkit.pop();
            cur_val=last_entry.get("1.0", END).replace('\n','');
            if(len(cur_val.strip())==0):
                cur_val=skip;
            old_entry=self.parent.controller.book.getEntry(row).getAttribute(col_name[col])
            if(not (old_entry.strip()==cur_val.strip())):
                last_entry.delete("2.0", END);
                last_entry.tag_add("a", "1.0", END);
                last_entry.tag_configure("a", background="skyblue");
                contact = self.parent.controller.book.getEntry(row);
                attr = col_name[col];
                contact.setAttribute(attr, cur_val);
                self.parent.controller.dirty=True;
                
        self.parent.controller.checkit.append([entry,r,c]);
        

    """
    Mehtod used to display conatacts on the home page
    ----------------------------------------------------------
        arguments: contacts => an array of AddressBookEnry objects

        return: none

        side affects: displays all contacts on screen.
    """
    def print_contacts(self, contacts):
        starttime = datetime.datetime.now()

        row = 0;

        for entry in self.parent.controller.book:
            column=0;
            current_row=[];
            for attr in col_name: 
                t = entry.getAttribute(attr);
                label = Text(self.interior, height=1, width=15);
                if t == skip:
                    label.insert(INSERT, "");
                else:
                    label.insert(INSERT, t);

                label.bind("<KeyRelease-Return>", lambda cmd, row=row, column=column, entry=label: self.update_contact(row, column, entry));
                label.bind("<Button-1>", lambda cmd, row=row, column=column, entry=label: self.redraw_entry(row, column, entry))
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                current_row.append(label);
                column += 1;

            row +=1;
        endtime = datetime.datetime.now()



    """
    Method used to print the resultf of a search
    -------------------------------------------------------------------------------
        arguments: contacts => and array returned from the search all fileds method
                               containing indexs for all contacts that match search.
        return: None

        side affects: Displays a sub set of the contacts, those that have 1 or more
                      filed that contained the search string.
    """
    def print_search_contacts(self, contacts):

        starttime = datetime.datetime.now()

        row = 0;

        for entry in self.parent.controller.search_contacts:
            column=0;
            current_row=[];

            for attr in col_name: 
                t = entry.getAttribute(attr);
                label = Text(self.interior, height=1, width=15);
                if t == skip:
                    label.insert(INSERT, "");
                else:
                    label.insert(INSERT, t);

                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                label.bind("<KeyRelease-Return>", lambda cmd, row=row, column=column, entry=label: self.update_contact(row, column, entry));
                label.bind("<Button-1>", lambda cmd, row=row, column=column, entry=label: self.redraw_entry(row, column, entry))
                current_row.append(label);
                column += 1;

            row +=1;

        endtime = datetime.datetime.now()




    """
    Method used to print the contacts for the delete page
    -------------------------------------------------------------------------------
        arguments: contacts => address book enerires array

        return: None

        side affects: Displays all the contacts in an address book with a check box next
                      to that contact to allow the user select which contacts to delete.
    """
    def print_delete_contact_page(self, contacts):
        row=0;
        index=0;
        for entry in self.parent.controller.book:
            column = 0;
            current_row=[];
            for attr in ["Delete", "FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"]:
                t=entry.getAttribute(attr);
                if attr=="Delete":
                    b = Checkbutton(self.interior, width=14, text=row, command=(lambda i=index: self.onPress(
                        i)));  # create check buttons in when we create the table, bind to onPress funtion
                    b.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                    b.deselect();
                    self.parent.controller.status.append(0);
                else:
                    t = entry.getAttribute(attr);
                    label = Text(self.interior, height=1, width=15);
                    if t == skip:
                        label.insert(INSERT, "");
                        label.config(state=DISABLED);
                    else:
                        label.insert(INSERT, t);
                        label.config(state=DISABLED);
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)

                column += 1;
            index += 1;
            row += 1;

        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        index = 0;