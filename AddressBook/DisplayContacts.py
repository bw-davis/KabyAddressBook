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
from platform import system as platformz


contacts = ["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Phone Number", "Email" ];
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"];


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

    def onPress(self, i):
        self.parent.controller.status[i] = 1;

    """
    Method used to handle if the user clicks the enter button after editing a contact info.
    ---------------------------------------------------------------------------------------
        arguments: row => the row this entry appears on in the displayed table
                   col
    """
    def update_contact(self, row, col, entry):
        #Up date contact
        #Change the background of the field
        attr = col_name[col];  # The contact attribute to be replaceed
        contact = self.parent.controller.book.getEntry(row);  # Contact to be modified
        contact_attr = contact.getAttribute(attr);  # The contact attribute to be replaced
        # print(contact_attr);
        new_contact_data = entry.get("1.0", END).replace('\n','');  # The text that has been entered in the Text widget. The end-1c ignores newline charater
        print(new_contact_data);
        #entry = Text(self.interior, height=1, width=15);
        entry.delete("1.0", END);
        entry.delete("2.0", END);
        entry.insert(INSERT, new_contact_data);
        # print(new_contact_data);
        entry.tag_add("a", "1.0", END);
        entry.tag_configure("a", background="skyblue");
        # entry.insert(INSERT, new_contact_data);
        #dirty.append([entry, row, col]);  # Keeping track of all unsaved entries.
        contact.setAttribute(attr, new_contact_data);
        self.parent.controller.dirty=True;
        #self.parent.controller.book.saveToFile(self.parent.controller.book_name);
        
       
    def redraw_entry(self, r, c, entry):
        #For editing update.
        #Redraw the blank
        val=entry.get("1.0", END);
        if(self.parent.controller.checkit):
            #print(self.parent.controller.checkit);
            last_entry, row, col = self.parent.controller.checkit.pop();
            cur_val=last_entry.get("1.0", END).replace('\n','');
            if(len(cur_val.strip())==0):
                cur_val=skip;
            print("not empty")
            print("need to redraw")
            old_entry=self.parent.controller.book.getEntry(row).getAttribute(col_name[col])
            print("old entry= {} | cur val= {}".format(old_entry, cur_val));
            print("old entry type = {} | cur val type = {}".format(type(old_entry), type(cur_val)));
            print("old_entry==cur_val={}".format(old_entry.strip()==cur_val.strip()));
            if(not (old_entry.strip()==cur_val.strip())):
                last_entry.delete("2.0", END);
                #last_entry.delete("1.0", END);
                last_entry.tag_add("a", "1.0", END);
                last_entry.tag_configure("a", background="skyblue");
                contact = self.parent.controller.book.getEntry(row);
                attr = col_name[col];
                contact.setAttribute(attr, cur_val);
                self.parent.controller.dirty=True;
                

        else:
            print("empty")

        print("Appending{}".format(val));
        self.parent.controller.checkit.append([entry,r,c]);
        

    def print_contacts(self, contacts):
        #For search result
        #print contacts into the table
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
        print (endtime - starttime)
        print("print entry time")

    def print_search_contacts(self, contacts):
        #For search result
        #print contacts into the table
        #print checkbox widgets
        starttime = datetime.datetime.now()

        row = 0;

        for entry in self.parent.controller.search_contacts:
            column=0;
            current_row=[];
            #sentry=self.parent.controller.book.getEntry(e);
            for attr in col_name: 
                t = entry.getAttribute(attr);
                label = Text(self.interior, height=1, width=15);
                if t == skip:
                    label.insert(INSERT, "");
                else:
                    label.insert(INSERT, t);

                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                current_row.append(label);
                column += 1;

            row +=1;

        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print("print entry time")



    def print_delete_contact_page(self, contacts):
        #DeletePage Frame
        row=0;
        index=0;
        for entry in self.parent.controller.book:
            column = 0;
            current_row=[];
            for attr in ["Delete", "FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone", "email"]:
                t=entry.getAttribute(attr);
                if attr=="Delete":
                    v = StringVar()
                    z = IntVar()
                    v.set("L");
                    # b=Radiobutton(self, text="", variable=v);
                    b = Checkbutton(self.interior, width=14, text=row, command=(lambda i=index: self.onPress(
                        i)));  # create check buttons in when we create the table, bind to onPress funtion
                    b.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                    self.parent.controller.status.append(0);
                    #print("now i am appending")
                else:
                    t = entry.getAttribute(attr);
                    #print("{} {} {}".format(t, row, column));
                    label = Text(self.interior, height=1, width=15);
                    if t == skip:
                        label.insert(INSERT, "");
                    else:
                        label.insert(INSERT, t);
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)

                column += 1;
            #self._widgets.append(current_row)
            index += 1;
            row += 1;

        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        index = 0;