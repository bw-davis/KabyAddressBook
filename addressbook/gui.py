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

            self.controller.book.saveToFile(self.controller.book_name);
            self.controller.refresh_frame(StartPage);
            self.controller.show_frame(StartPage);
            self.controller.delete_status=[]
        else:
            # if user cancels
            print("No")




class BlankPage(tk.Frame):
    #SearchResultPage Frame
    def __init__(self, parent, controller):
        starttime = datetime.datetime.now()


        tk.Frame.__init__(self, parent)


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
        editmenu.add_command(label="Add", command=lambda: controller.show_frame(controller.refresh_frame(PageOne)));
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


        #print("\n\nLen of contacts = {}\n\n".format(len(self.controller.book)));
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
        if(self.controller.dirty):
            if messagebox.askokcancel("Quit", "Want to save unsaved data?"):
                self.controller.book.saveToFile(self.controller.book_name);
                root.destroy();
            else:
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
        if(self.controller.dirty):
            if messagebox.askokcancel("Quit", "Want to save unsaved data?"):
                self.controller.book.saveToFile(self.controller.book_name);
                self.controller.destroy();
            else:
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
        print("var is {}".format(var));
        if var == "Name":
            print("sorting by name");
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
        FileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".tsv")])
        if FileName!="":
            FileName +=".kab"
            self.controller.book.saveNewFile(FileName);
            newApp = KabyAddrapp(FileName);
            newApp.mainloop();
        print(FileName)



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

        importFileName = tkinter.filedialog.askopenfilename()
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
                 try_again=askokcancel("Warning", "This is not a standard .tsv file,\n do you still want to import that")
                 if try_again:

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
        exportFileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".tsv")])+".tsv"
        self.controller.book.exportToFile(exportFileName);
        


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
        #to open an existing  .kab file
        AddressbookName = tkinter.filedialog.askopenfilename()
        app2 = KabyAddrapp(AddressbookName);
        app2.protocol("WM_DELETE_WINDOW", lambda: self.exit_app(app2));
        app2.mainloop();
        print(AddressbookName)


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
        print("savefile")
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
        FileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".tsv")])+".kab"
        print(FileName)
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

        if(((len(results)) > 1) and name):
            print(len(results))

            for i in results:
                #print(i);
                #print(self.controller.book.getEntry(i));
                self.controller.search_contacts.append(self.controller.book.getEntry(i));
            
            self.controller.refresh_frame(SearchResultPage);
            print("Im going to the search page")
            print("name = {}".format(name))
            self.controller.show_frame(SearchResultPage)
        else:
            print("Staying");
            self.controller.show_frame(StartPage)

        


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        print("im in PageOne");
        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller;

        new_contact = []

        fname = StringVar();
        lname = StringVar();
        email = StringVar();
        address = StringVar();
        state = StringVar();
        zipC = StringVar();
        phone = StringVar();

        # Collect first name from user.
        tk.Label(self, text="First name").grid(column=2, row=2, sticky=(W, E))
        first_name = ttk.Entry(self, width=7, textvariable=fname);
        first_name.insert(INSERT, "");
        first_name.grid(column=2, row=3, sticky=(W, E));
        # new_contact.append(fname);

        # Collect last name from user.
        tk.Label(self, text="Last name").grid(column=3, row=2, sticky=(W, E))
        last_name = ttk.Entry(self, width=7, textvariable=lname);
        last_name.grid(column=3, row=3, sticky=(W, E));
        # new_contact.append(lname);


        # Collect address from user
        tk.Label(self, text="Address").grid(column=2, row=4, sticky=(W, E))
        addr = ttk.Entry(self, width=7, textvariable=address);
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
        st = ttk.Entry(self, width=25, textvariable=state);
        st.grid(column=3, row=7, sticky=(W, E));
        # new_contact.append(state);

        # Collect zip from user
        tk.Label(self, text="Zip Code").grid(column=2, row=8, sticky=(W, E))
        zip_code = ttk.Entry(self, width=25, textvariable=zipC);
        zip_code.grid(column=2, row=9, sticky=(W, E));
        # new_contact.append(zipC);

        # Collect zip from user
        tk.Label(self, text="Phone Number").grid(column=2, row=10, sticky=(W, E))
        phone_number= ttk.Entry(self, width=25, textvariable=phone);
        phone_number.grid(column=2, row=11, sticky=(W, E));

        # Collect email from user.
        tk.Label(self, text="Email").grid(column=3, row=10, sticky=(W, E))
        em = ttk.Entry(self, width=7, textvariable=email);
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



def on_closing(root):
    if(root.dirty):
            if messagebox.askokcancel("Quit", "Want to save unsaved data?"):
                root.destroy();
    else:
        #print("Nothing to save, quiting")
        root.destroy();



def main():
    app = KabyAddrapp();
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app));
    starttime = datetime.datetime.now()

    app.mainloop();
    endtime = datetime.datetime.now()
    print (endtime - starttime)


if __name__ == "__main__":
    main()
