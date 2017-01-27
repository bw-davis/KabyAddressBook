from tkinter import *
import tkinter as tk 
from tkinter import ttk
import tkinter.filedialog 
from tkinter.messagebox import *
from AddressBook import *
from tkinter import messagebox

#contacts=["First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Email", "Phone Number"];
#col_name = ["FirstName", "LastName", "Address1", "City", "Zipcode", "Phone"];
contacts=["First name", "Last name", "Address1", "Address2", "City", "State", "Zip","Phone Number"];
col_name = ["FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone"];
book = AddressBook()
book.importFromFile("SavedAddressBook.tsv")

dirty=[]; #And array of arrays of[label, row, col] of all "dirty" or modified text widgets
states=[] #record index of the conetancts that you want to delete
print("I cleaned states in");
edited=False;
skip = "#skip"

class KabyAddrapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        #states=[] #record delete indexs
        #print("I cleaned states ");
        if(len(args)==1):
            print("book");
        else:
            print("need to make a book");

        tk.Tk.__init__(self, *args, **kwargs);
        self.container = tk.Frame(self); 

        self.container.grid(row=0, ipadx=25, ipady=10);

        self.container.grid_rowconfigure(0,weight=1);
        self.container.grid_columnconfigure(0,weight=1);
        
        self.frames= {};
        
        for F in (StartPage, PageOne, DeletePage):
            if F==DeletePage:
                print("initialize StartPage")
            if F==DeletePage:
                print("initialize PageOne")
            if F==DeletePage:
                print("initialize DeletePage")
            frame = F(self.container, self);
            self.frames[F] = frame;
            frame.grid(row=0, column=0, sticky="nsew");
        #states=[] #record delete index
        #print("I cleaned states 2");
        self.show_frame(StartPage);

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


def NewContact():
    print("donothing");

def importFile():
    print("dosomething");
    importFileName=tkinter.filedialog.askopenfilename()
    print (importFileName)

def exportFile():
    print("dosomething");
    importFileName=tkinter.filedialog.askopenfilename()
    print (exportFileName)

def openAddressBook():
    #print("dosomething");
    AddressbookName=tkinter.filedialog.askopenfilename()
    book2 = AddressBook()
    book2.importFromFile("SavedAddressBook.tsv")
    app2=KabyAddrapp(AddressbookName);
    app2.mainloop();
    print (AddressbookName)

def save():
    #print("dosomething");
    print("savefile")
    book.exportToFile("SavedAddressBook.tsv");

def saveAs():
    #print("dosomething");
    FileName=tk.filedialog.asksaveasfilename(filetypes=[("text",".tsv")])
    print (FileName)
    book.exportToFile(FileName);





class SimpleTable2(tk.Frame):
    def __init__(self, parent):
        print("im in SimpleTable2");
        states=[];
        self._widgets=[];
        tk.Frame.__init__(self, parent, background='black');
        self._widgets = []

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    def onPress(self,i):
        states[i]= 1;


    def print_contacts(self, contacts):
        #states=[];
        
        #print("I cleaned states 3");
        col_name = ["Delete","FirstName", "LastName", "Address1", "Address2", "City", "State", "Zipcode", "Phone"];
        row=0;
        column=0
        current_row = []
        index=0;
        #for c in ["Delete","First name", "Last name", "Address1", "Address2", "City", "State", "Zip", "Email", "Phone Number"]:
        for c in col_name:
            label=Text(self, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)
            column+=1;
        row+=1;


        for entry in book:
            column=0;
            current_row=[];
            #for attr in ["button","FirstName", "LastName", "Address1", "City", "Zipcode", "Phone"]:
                #if(attr=="button"):
            for attr in col_name:
                if(attr=="Delete"):
                    print("button")
                    v=StringVar()
                    z=IntVar()
                    v.set("L");
                    #b=Radiobutton(self, text="", variable=v);
                    b=Checkbutton(self, text=row,command=(lambda i=index:self.onPress(i)));#creat check buttons in when we create the table, bind to onPress funtion
                    b.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                    states.append(0);
                    print("now i am appending")


                else:
                    t=entry.getAttribute(attr);
                    print("{} {} {}".format(t, row, column));
                    label=Text(self, height=1, width=15);
                    if t == skip:
                        label.insert(INSERT, "");
                    else:
                        label.insert(INSERT, t);
                    label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                    current_row.append(label)

                column+=1;
            self._widgets.append(current_row)
            index+=1;
            row+=1;
        print(states)


            

        for column in range(7):
            self.grid_columnconfigure(column, weight=1)
        index=0;


class SimpleTable(tk.Frame):
    def __init__(self, parent):
        print("im in SimpleTable1");
        self._widgets=[];
        tk.Frame.__init__(self, parent, background='black');
        self._widgets = []
        #states=[] #record delete index
        #print("I cleaned states 4");


    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

    #Gets text from text box, finds proper contact and contact information to replace.
    def update_contact(self, row, col, entry):
        #print("{} {}".format(row, col));
        #print(book.getEntry(row).getAttribute(col_name[col]));
        attr = col_name[col]; # The contact attribute to be replaceed
        contact = book.getEntry(row-1); #Contact to be modified
        contact_attr = contact.getAttribute(attr); #The contact attribute to be replaced
        #print(contact_attr);
        new_contact_data = entry.get("1.0", END).replace('\n', ''); #The text that has been entered in the Text widget. The end-1c ignores newline charater
        #print(new_contact_data);
        entry.delete("2.0", END);
        entry.tag_add("a", "1.0", END);
        entry.tag_configure("a", background="skyblue");
        #entry.insert(INSERT, new_contact_data);
        dirty.append([entry, row, col]); #Keeping track of all unsaved enteiries.
        contact.setAttribute(attr, new_contact_data);
        book.exportToFile("SavedAddressBook.tsv");


    def print_contacts(self, contacts):
        row=0;
        column=0
        current_row = []
        for c in contacts:
            label=Text(self, height=1, width=15);
            label.insert(INSERT, c);
            label.config(state=DISABLED);
            label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
            self._widgets.append(current_row)
            column+=1;
        row+=1;

        for entry in book:
            column=0;
            current_row=[];
            for attr in col_name:
                t=entry.getAttribute(attr);
                #print("{} {} {}".format(t, row, column));
                label=Text(self, height=1, width=15);
                if t == skip:
                    label.insert(INSERT, "");
                else:
                    label.insert(INSERT, t);
                label.bind("<KeyRelease-Return>", lambda cmd, row=row, column=column, entry=label: self.update_contact(row, column, entry));
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1);
                current_row.append(label);
                column+=1;
            self._widgets.append(current_row)
            row+=1;

            
        #Adds padding around contact info
        for column in range(7):
            self.grid_columnconfigure(column, weight=1)

    def toDelete():
        #tast case for delete
        pass


class DeletePage(tk.Frame):


    def __init__(self, parent, controller):
        print("im in DeletePage");
        tk.Frame.__init__(self, parent)
        self.parent=parent;
        self.controller = controller;
        states=[] #record delete index
        #print("I cleaned states 5");


        sort_label=ttk.Label(self, text="Sort by:");
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
        #ttk.Button(self, text="Cancle", command=).grid(row=3, column=2);
        ttk.Button(self, text="Cancle", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=2, stick='w');

    def delete_confirm(self):
        #the function that will be involk when user click Delete button in delete page
        index=0
        count =0
        print("donsomething2");
        print(states);
        if askokcancel("Delete","Are you sure to Delete selected Data?"):
            # pop a diolog let user to confirm
            print("yes")
            #if yes, delete contacts
            for i in states:
                if i !=0:
                    print("should delete No.")
                    print(index+1)
                    book.removeEntry(index-count);
                    count+=1
                index+=1;

            book.exportToFile("SavedAddressBook.tsv");
            self.controller.refresh_frame(StartPage);
            self.controller.show_frame(StartPage);
        else:
            #if user cancles
            print("No")


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        print("im in StartPage");
        tk.Frame.__init__(self, parent)
        self.parent=parent;
        self.controller = controller;
        #reset array states for next delete operation
        #states =[]
        #print("I cleaned states 6");
        #resetDeletePage
        #self.controller.refresh_frame(DeletePage);

        #File tab on menu bar
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


        #Edit tab on menu bar
        editmenu=Menu(menubar, tearoff=0);
        menubar.add_cascade(label="Edit", menu=editmenu);
        #editmenu.add_command(label="Undo", command=donothing);
        addmenu=Menu(menubar, tearoff=0);
        #menubar.add_cascade(label="Add", menu=addmenu);
        editmenu.add_command(label="Add", command=lambda: controller.show_frame(PageOne));
        #editmenu.add_command(label="Delete", command=lambda: controller.show_frame(DeletePage));
        editmenu.add_command(label="Delete", command=self.to_delete_page);



         #Sort by meu
        sort_label=ttk.Label(self, text="Sort by:");
        sort_label.grid(row=0, column=6, stick="e");
        var = StringVar(self);
        options = ["Name", "Zip"];
        var.set(options[0]);
        dropdown = ttk.OptionMenu(self, var, options[0], *options, command=lambda cmd, var=var: self.sort(var.get()));
        dropdown.grid(row=0, column=7, sticky="w");


        
        t = SimpleTable(self);
        t.grid(row=1, column=0, columnspan=8, padx=20);
        t.print_contacts(contacts);

    def sort(self, var):
        print("var is {}".format(var));
        if var=="Name":
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
        states=[] #record delete index
        print("I cleaned states 7");
        self.controller.refresh_frame(DeletePage);
        print("Im going to the delete page")
        self.controller.show_frame(DeletePage)




        


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        print("im in PageOne");
        tk.Frame.__init__(self, parent)
        self.parent=parent;
        self.controller = controller;


        new_contact =[]


        fname=StringVar();
        lname=StringVar();
        email=StringVar();
        address=StringVar();
        state=StringVar();
        zipC=StringVar();
        phone=StringVar();

        #Collect first name from user.
        tk.Label(self, text="first name").grid(column=2, row=2, sticky=(W, E))
        first_name=ttk.Entry(self, width=7, textvariable=fname);
        first_name.insert(INSERT, "");
        first_name.grid(column=2, row=3, sticky=(W, E));
        #new_contact.append(fname);

        #Collect last name from user.
        tk.Label(self, text="last name").grid(column=3, row=2, sticky=(W, E))
        last_name=ttk.Entry(self, width=7, textvariable=lname);
        last_name.grid(column=3, row=3, sticky=(W, E));
        #new_contact.append(lname);

        #Collect email from user.
        tk.Label(self, text="email").grid(column=2, row=4, sticky=(W, E))
        em=ttk.Entry(self, width=7, textvariable=email);
        em.grid(column=2, row=5, sticky=(W, E));
        #new_contact.append(email);

        #Collect address from user
        tk.Label(self, text="Address").grid(column=2, row=6, sticky=(W, E))
        addr=ttk.Entry(self, width=7, textvariable=address);
        addr.grid(column=2, row=7, sticky=(W, E));
        #new_contact.append(address);

        #Collect state from user
        tk.Label(self, text="State").grid(column=3, row=10, sticky=(W, E))
        st=ttk.Entry(self, width=25, textvariable=state);
        st.grid(column=3, row=11, sticky=(W, E));
        #new_contact.append(state);

        #Collect zip from user
        tk.Label(self, text="Zip Code").grid(column=2, row=8, sticky=(W, E))
        zip_code=ttk.Entry(self, width=25, textvariable=zipC);
        zip_code.grid(column=2, row=9, sticky=(W, E));
        #new_contact.append(zipC);

        #Collect city from user7
        tk.Label(self, text="City").grid(column=3, row=8, sticky=(W, E))
        city=ttk.Entry(self, width=7);
        city.grid(column=3, row=9, sticky=(W, E));
        #new_contact.append(zipC);
        
        #Collect zip from user
        tk.Label(self, text="Phone Number").grid(column=2, row=10, sticky=(W, E))
        phone_number=ttk.Entry(self, width=25, textvariable=phone);
        phone_number.grid(column=2, row=11, sticky=(W, E));
        #new_contact.append(phone);
        tk.Label(self, text="Address2").grid(column=3, row=6, sticky=(W, E))
        phone_number=ttk.Entry(self, width=25);
        phone_number.grid(column=3, row=7, sticky=(W, E));

        #Bind Enter to create customer as well.

        #ttk.Button(self, text="submit", command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(), state.get(), zipC.get(), em.get(), phone.get())).grid(column=2, row=12);
        ttk.Button(self, text="submit", command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(),"",city.get(), state.get(), zipC.get(), em.get(), phone.get())).grid(column=2, row=12);
        ttk.Button(self, text="cancle", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=12);

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5);



    #AddressBookEnetry(FirstName, LastName, Address1, Address2, City, State, Zipcode, Phone)
    def add_contact(self, fname, lname, address1, address2, city, state, zipC, email, phone):
        el = [fname, lname, address1, address2, city, state, zipC, email];
        new=[x if not x=="" else "#skip" for x in el]
        print(new)


        print("fname={} lname={}".format(type(fname), lname));
        #new_contact=AddressBookEntry(fname, lname, address1, address2, city, state, zipC, phone); 
        new_contact=AddressBookEntry(*new);
        book.addEntry(new_contact);
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);
        book.exportToFile("SavedAddressBook.tsv");

def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def main():
    app=KabyAddrapp();
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app));
    app.mainloop();


if __name__ == "__main__":
    main()



