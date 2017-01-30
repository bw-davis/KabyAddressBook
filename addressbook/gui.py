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
# contacts=["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Email", "Phone Number"];
# col_name = ["FirstName", "LastName", "Address1", "City", "Zipcode", "Phone"];
contacts = ["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Phone Number"];
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone"];
book = AddressBook()
book.importFromFile("SavedAddressBook.tsv")

dirty = [];  # And array of arrays of[label, row, col] of all "dirty" or modified text widgets
states = []  # record index of the contacts that you want to delete
print("I cleaned states in");
edited = False;
skip = "#skip"
starttime = datetime.datetime.now()
endtime = datetime.datetime.now()



class KabyAddrapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        #if platform() == 'Darwin':  # How Mac OS X is identified by Python
            #system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')

        # states=[] #record delete indexes
        # print("I cleaned states ");
        if (len(args) == 1):
            print("book");
            book.importFromFile(args[0]); 
        else:
            print("need to make a book");

        tk.Tk.__init__(self, *args, **kwargs);
        self.container = tk.Frame(self);

        self.container.grid(row=0, ipadx=25, ipady=10);

        self.container.grid_rowconfigure(0, weight=1);
        self.container.grid_columnconfigure(0, weight=1);

        self.frames = {};

        for F in (StartPage,PageOne):
            starttime = datetime.datetime.now()
            if F == DeletePage:
                print("initialize StartPage")
            if F == DeletePage:
                print("initialize PageOne")
            if F == DeletePage:
                print("initialize DeletePage")
            frame = F(self.container, self);
            self.frames[F] = frame;
            frame.grid(row=0, column=0, sticky="nsew");

            endtime = datetime.datetime.now()
            print (endtime - starttime)



        #starttime = datetime.datetime.now()
        #init Start page here
        #frame = StartPage(self.container, self);
        #self.frames[StartPage] = frame;
        #frame.grid(row=0, column=0, sticky="nsew");


        print("StartPage initialize time")





        # states=[] #record delete index
        # print("I cleaned states 2");
        starttime = datetime.datetime.now()
        #self.refresh_frame(StartPage);
        self.show_frame(StartPage);

        #self.show_frame(StartPage);
        #self.refresh_frame(StartPage);
        #self.show_frame(StartPage);

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


def donothing():
    print("donothing");
    print(tkinter.messagebox.showinfo("messagebox","welcome to the Kaby Address Book"))


def NewContact():
    print("donothing");


def importFile():
    print("dosomething");
    importFileName = tkinter.filedialog.askopenfilename()
    print(importFileName)


def exportFile():
    print("dosomething");
    importFileName = tkinter.filedialog.askopenfilename()
    print(exportFileName)


def openAddressBook():
    # print("dosomething");
    AddressbookName = tkinter.filedialog.askopenfilename()
    app2 = KabyAddrapp(AddressbookName);
    app2.mainloop();
    print(AddressbookName)


def save():
    # print("dosomething");
    print("savefile")
    book.exportToFile("SavedAddressBook.tsv");


def saveAs():
    # print("dosomething");
    FileName = tk.filedialog.asksaveasfilename(filetypes=[("text", ".tsv")])
    print(FileName)
    book.exportToFile(FileName);





class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

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

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    def print_contacts(self, contacts):
        #for row in range(10,100):
            #for col in range(5):
                #l = Label(self.interior, text="   row:{} col:{}  ".format(row, col))
                #l.grid(row=row, column=col, padx=1, pady=1);

        starttime = datetime.datetime.now()

        row = 0;
        #column=0;
        #current_row=[];
        #for c in contacts: 
            #label = Label(self.interior, text=c);
           # label.grid(row=row, column=column, sticky='nsew', padx=1, pady=1);
           #column +=1;
       #row +=1;

        for entry in book:
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
                current_row.append(label);
                column += 1;

            row +=1;

        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print("print entry time")



class SimpleTable2(tk.Frame):
    def __init__(self, parent):
        print("im in SimpleTable2");
        states = [];
        self._widgets = [];
        tk.Frame.__init__(self, parent, background='black');
        self._widgets = []

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    def onPress(self, i):
        states[i] = 1;

    def print_contacts(self, contacts):
        # states=[];

        # print("I cleaned states 3");
        col_name = ["Delete", "FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone"];
        row = 0;
        column = 0
        current_row = []
        index = 0;
        starttime = datetime.datetime.now()

        # for c in ["Delete","First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Email", "Phone Number"]:
        for c in col_name:
            label = Text(self, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)
            column += 1;
        row += 1;

        for entry in book:
            column = 0;
            current_row = [];
            # for attr in ["button","FirstName", "LastName", "Address1", "City", "Zipcode", "Phone"]:
            # if(attr=="button"):
            for attr in col_name:
                if (attr == "Delete"):
                    print("button")
                    v = StringVar()
                    z = IntVar()
                    v.set("L");
                    # b=Radiobutton(self, text="", variable=v);
                    b = Checkbutton(self, text=row, command=(lambda i=index: self.onPress(
                        i)));  # create check buttons in when we create the table, bind to onPress funtion
                    b.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                    states.append(0);
                    print("now i am appending")


                else:
                    t = entry.getAttribute(attr);
                    print("{} {} {}".format(t, row, column));
                    label = Text(self, height=1, width=15);
                    if t == skip:
                        label.insert(INSERT, "");
                    else:
                        label.insert(INSERT, t);
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)

                column += 1;
            self._widgets.append(current_row)
            index += 1;
            row += 1;
        print(states)

        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        index = 0;

        endtime = datetime.datetime.now()
        print (endtime - starttime)


class SimpleTable(tk.Frame):
    def __init__(self, parent):
        print("im in SimpleTable1");
        self._widgets = [];
        tk.Frame.__init__(self, parent, background='black');
        self._widgets = []
        # states=[] #record delete index
        # print("I cleaned states 4");

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    # Gets text from text box, finds proper contact and contact information to replace.
    def update_contact(self, row, col, entry):
        # print("{} {}".format(row, col));
        # print(book.getEntry(row).getAttribute(col_name[col]));
        attr = col_name[col];  # The contact attribute to be replaceed
        contact = book.getEntry(row - 1);  # Contact to be modified
        contact_attr = contact.getAttribute(attr);  # The contact attribute to be replaced
        # print(contact_attr);
        new_contact_data = entry.get("1.0", END).replace('\n','');  # The text that has been entered in the Text widget. The end-1c ignores newline charater
        # print(new_contact_data);
        entry.delete("2.0", END);
        entry.tag_add("a", "1.0", END);
        entry.tag_configure("a", background="skyblue");
        # entry.insert(INSERT, new_contact_data);
        dirty.append([entry, row, col]);  # Keeping track of all unsaved entries.
        contact.setAttribute(attr, new_contact_data);
        book.exportToFile("SavedAddressBook.tsv");

    def print_contacts(self, contacts):
        starttime = datetime.datetime.now()

        row = 0;
        column = 0
        current_row = []
        for c in contacts:
            label = Text(self, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)
            column += 1;
        row += 1;

        for entry in book:
            column = 0;
            current_row = [];
            for attr in col_name:
                t = entry.getAttribute(attr);
                # print("{} {} {}".format(t, row, column));
                label = Text(self, height=1, width=15);
                if t == skip:
                    label.insert(INSERT, "");
                else:
                    label.insert(INSERT, t);
                label.bind("<KeyRelease-Return>",
                           lambda cmd, row=row, column=column, entry=label: self.update_contact(row, column, entry));
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                current_row.append(label);
                column += 1;
            self._widgets.append(current_row)
            row += 1;

        # Adds padding around contact info
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)

        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print ("table time")

    def toDelete(self):
        # tast case for delete
        pass


class DeletePage(tk.Frame):
    def __init__(self, parent, controller):
        print("im in DeletePage");
        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller;
        states = []  # record delete index
        # print("I cleaned states 5");


        sort_label = ttk.Label(self, text="Sort by:");
        sort_label.grid(row=0, column=6, stick="e");
        var = StringVar(self);
        options = ["Name", "Zip"];
        var.set(options[0]);
        dropdown = ttk.OptionMenu(self, var, options[0], *options);
        dropdown.grid(row=0, column=7, sticky="w");

        t = SimpleTable2(self);
        t.grid(row=1, column=0, columnspan=8, padx=20);
        t.print_contacts(contacts);

        ttk.Button(self, text="Delete", command=lambda: self.delete_confirm()).grid(row=2, column=2, stick='e');
        # ttk.Button(self, text="Cancel", command=).grid(row=3, column=2);
        ttk.Button(self, text="Cancel", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=2,
                                                                                               stick='w');

    def delete_confirm(self):
        # the function that will be evoked when user click Delete button in delete page
        index = 0
        count = 0
        print("donsomething2");
        print(states);
        if askokcancel("Delete", "Are you sure to Delete selected Data?"):
            # pop a dialog let user to confirm
            print("yes")
            # if yes, delete contacts
            for i in states:
                if i != 0:
                    print("should delete No.")
                    print(index + 1)
                    book.removeEntry(index - count);
                    count += 1
                index += 1;

            book.exportToFile("SavedAddressBook.tsv");
            self.controller.refresh_frame(StartPage);
            self.controller.show_frame(StartPage);
        else:
            # if user cancels
            print("No")
class BlankPage(tk.Frame):
    def __init__(self, parent, controller):
        starttime = datetime.datetime.now()

        print("im in StartPage");

        tk.Frame.__init__(self, parent)

 


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        starttime = datetime.datetime.now()

        print("im in StartPage");

        tk.Frame.__init__(self, parent)
        self.parent = parent;
        self.controller = controller;
        # reset array states for next delete operation
        # states =[]
        # print("I cleaned states 6");
        # resetDeletePage
        # self.controller.refresh_frame(DeletePage);

        # File tab on menu bar
        #print(askokcancel("Delete", "Are you sure to Delete selected Data?"))
        #showinfo("Say Hello", "Hello World")
        #tkinter.messagebox.showinfo("messagebox","this is button 2 dialog")  

        print(states)
        menubar = Menu(parent.master);
        parent.master.config(menu=menubar);
        filemenu = Menu(menubar, tearoff=0);
        menubar.add_cascade(label="File", menu=filemenu);
        filemenu.add_command(label="New", command=donothing);
        filemenu.add_command(label="Open", command=openAddressBook);
        filemenu.add_command(label="Save", command=save);
        filemenu.add_command(label="Save as", command=saveAs);
        filemenu.add_command(label="Import", command=importFile);
        filemenu.add_command(label="Export", command=exportFile);
        filemenu.add_separator();
        filemenu.add_command(label="Exit", command=quit);

        # Edit tab on menu bar
        editmenu = Menu(menubar, tearoff=0);
        menubar.add_cascade(label="Edit", menu=editmenu);
        # editmenu.add_command(label="Undo", command=donothing);
        addmenu = Menu(menubar, tearoff=0);
        # menubar.add_cascade(label="Add", menu=addmenu);
        editmenu.add_command(label="Add", command=lambda: controller.show_frame(PageOne));
        # editmenu.add_command(label="Delete", command=lambda: controller.show_frame(DeletePage));
        editmenu.add_command(label="Delete", command=self.to_delete_page);

        # Sort by meu
        sort_label = ttk.Label(self, text="Sort by:");
        sort_label.grid(row=0, column=6, stick="e");
        var = StringVar(self);
        options = ["Name", "Zip"];
        var.set(options[0]);
        dropdown = ttk.OptionMenu(self, var, options[0], *options, command=lambda cmd, var=var: self.sort(var.get()));
        dropdown.grid(row=0, column=7, sticky="w");

        #t = SimpleTable(self);
        #t.grid(row=1, column=0, columnspan=8, padx=20);
        #t.print_contacts(contacts);

        contact_info = Frame(self, background='black');
        contact_info.grid(row=1, column=0, columnspan=8);
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

        f=VerticalScrolledFrame(self);
        f.grid(row=2, column=0, columnspan=8, padx=20);
        f.print_contacts(contacts);
        self.parent.update_idletasks();


        endtime = datetime.datetime.now()
        print (endtime - starttime)
        print("now im here")

    def sort(self, var):
        print("var is {}".format(var));
        if var == "Name":
            print("sorting by name");
            book.sortByName();
        else:
            print("sorting by zip");
            book.sortByZipcode();
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);

    def to_delete_page(self):
        # click delete in menu bar
        global states
        states = []  # record delete index
        print("I cleaned states 7");
        self.controller.refresh_frame(DeletePage);
        print("Im going to the delete page")
        self.controller.show_frame(DeletePage)


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
        tk.Label(self, text="first name").grid(column=2, row=2, sticky=(W, E))
        first_name = ttk.Entry(self, width=7, textvariable=fname);
        first_name.insert(INSERT, "");
        first_name.grid(column=2, row=3, sticky=(W, E));
        # new_contact.append(fname);

        # Collect last name from user.
        tk.Label(self, text="last name").grid(column=3, row=2, sticky=(W, E))
        last_name = ttk.Entry(self, width=7, textvariable=lname);
        last_name.grid(column=3, row=3, sticky=(W, E));
        # new_contact.append(lname);

        # Collect email from user.
        tk.Label(self, text="email").grid(column=2, row=4, sticky=(W, E))
        em = ttk.Entry(self, width=7, textvariable=email);
        em.grid(column=2, row=5, sticky=(W, E));
        # new_contact.append(email);

        # Collect address from user
        tk.Label(self, text="Address").grid(column=2, row=6, sticky=(W, E))
        addr = ttk.Entry(self, width=7, textvariable=address);
        addr.grid(column=2, row=7, sticky=(W, E));
        # new_contact.append(address);

        # Collect state from user
        tk.Label(self, text="State").grid(column=3, row=10, sticky=(W, E))
        st = ttk.Entry(self, width=25, textvariable=state);
        st.grid(column=3, row=11, sticky=(W, E));
        # new_contact.append(state);

        # Collect zip from user
        tk.Label(self, text="Zip Code").grid(column=2, row=8, sticky=(W, E))
        zip_code = ttk.Entry(self, width=25, textvariable=zipC);
        zip_code.grid(column=2, row=9, sticky=(W, E));
        # new_contact.append(zipC);

        # Collect city from user7
        tk.Label(self, text="City").grid(column=3, row=8, sticky=(W, E))
        city = ttk.Entry(self, width=7);
        city.grid(column=3, row=9, sticky=(W, E));
        # new_contact.append(zipC);

        # Collect zip from user
        tk.Label(self, text="Phone Number").grid(column=2, row=10, sticky=(W, E))
        phone_number= ttk.Entry(self, width=25, textvariable=phone);
        phone_number.grid(column=2, row=11, sticky=(W, E));

        # new_contact.append(phone);
        tk.Label(self, text="Address2").grid(column=3, row=6, sticky=(W, E))
        address2= ttk.Entry(self, width=25);
        address2.grid(column=3, row=7, sticky=(W, E));

        # Bind Enter to create customer as well.

        # ttk.Button(self, text="submit", command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(), state.get(), zipC.get(), em.get(), phone.get())).grid(column=2, row=12);
        ttk.Button(self, text="submit",
                   command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(),address2.get() , city.get(),
                                                    state.get(), zipC.get(), em.get(), phone.get())).grid(column=2,
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

        len_list=[len(x) for x in temp_list]

        if len_list[0]+len_list[1] > 0:
            print("we have a name")

        if sum(len_list[2:])+len(email)>0:
            print("we have another field")


        if not ((len_list[0]+len_list[1] > 0) and (sum(len_list[2:])+len(email)>0)):
            print("we don't have both a name and an additional field")
            showerror("Error","Error: Please enter a name (at least first or last) AND one additional field.\nPlease fix this before saving.")
            return


        list_with_skips = [x if not x == "" else "#skip" for x in temp_list]

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
        new_contact = AddressBookEntry(*list_with_skips, email=email);
        book.addEntry(new_contact);
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);
        book.exportToFile("SavedAddressBook.tsv");

    def valid_phone_number(self, number):
        """
        Function to test whether or not a phone number is valid.
        Args:
            number: the phone number

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
        return re.match("([0-9 a-z]+)([@]+)([0-9 a-z]+)([.]+)([0-9a-z]+)", email) != None


    def valid_zip(self, zipcode):
        # checking validation of Zipcode
        # format:<5 digits>
        #       <5 digits><-><4 digits>
        # good example: 97401
        #              97401-1234

        return re.match("([0-9]){5}([-]{1})([0-9]){4}$", zipcode) != None or re.match("([0-9 a-z]){5}$",zipcode) != None



def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def main():
    app = KabyAddrapp();
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app));
    starttime = datetime.datetime.now()

    

    app.mainloop();
    endtime = datetime.datetime.now()
    print (endtime - starttime)


if __name__ == "__main__":
    main()
