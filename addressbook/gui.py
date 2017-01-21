from tkinter import *
import tkinter as tk 
from tkinter import ttk
from AddressBook import *

contacts=["First name", "Last name", "Address", "State", "Zip", "Email", "Phone Number"];
book = AddressBook()
book.importFromFile("SavedAddressBook.txt")

class KabyAddrapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        
        if(len(args)==1):
            print("book");
        else:
            print("need to make a book");

        tk.Tk.__init__(self, *args, **kwargs);
        #This command will add logo
        #tk.Tk.conbitmap(self, default="");
        self.container = tk.Frame(self); 

        #container.pack(side="top", fill="both", expand=True);
        self.container.grid(row=0, ipadx=25, ipady=10);

        self.container.grid_rowconfigure(0,weight=1);
        self.container.grid_columnconfigure(0,weight=1);
        
        self.frames= {};
        
        for F in (StartPage, PageOne):
            frame = F(self.container, self);
            self.frames[F] = frame;
            frame.grid(row=0, column=0, sticky="nsew");

        self.show_frame(StartPage);

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


#class dropDown(tk.Frame):
    #def __init__(self, parent, var, 



class SimpleTable(tk.Frame):
    def __init__(self, parent):
        #self.contacts=[];
        self._widgets=[];
        # use black background so it "peeks through" to 
        # form grid lines
        tk.Frame.__init__(self, parent, background='black');
        self._widgets = []

    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)


    #def add_contact(self, contact_info):
        #self.contacts.append(contact_info);

    #def print_contacts(self, contacts):
        #row=0;
        #cntr=0;
        #for r in contacts:
            #column=0
            #current_row = []
            #for c in r:
                #print("{} {} {}".format(c, row, column))
                #label = tk.Label(self, text=c, borderwidth=0, width=15)
                #label=Text(self, height=1, width=15);
                #label.insert(INSERT, c);
                #if(row==0):
                    #label.config(state=DISABLED);
                #label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                #current_row.append(label)
                #column+=1;
            #self._widgets.append(current_row)
            #row+=1;

    def print_contacts(self, contacts):
        row=0;
        column=0
        current_row = []
        for c in contacts:
            #print("{} {} {}".format(c, row, column));
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
            for attr in ["FirstName", "LastName", "Address", "CityState", "Zipcode", "Email"]:
                t=entry.getAttribute(attr);
                print("{} {} {}".format(t, row, column));
                label=Text(self, height=1, width=15);
                label.insert(INSERT, t);
                label.grid(row=row, column=column, sticky="nsew", padx=1, pady=1)
                current_row.append(label)
                column+=1;
            self._widgets.append(current_row)
            row+=1;

            

        for column in range(7):
            self.grid_columnconfigure(column, weight=1)



class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        fname=StringVar();
        lname=StringVar();
        email=StringVar();
        address=StringVar();
        state=StringVar();
        zipC=StringVar();
        phone_number=StringVar();
        email=StringVar();

        #File tab on menu bar
        menubar = Menu(parent.master);
        parent.master.config(menu=menubar);
        filemenu = Menu(menubar, tearoff=0);
        menubar.add_cascade(label="File", menu=filemenu);
        filemenu.add_command(label="New", command=donothing);
        filemenu.add_command(label="Open", command=donothing);
        filemenu.add_command(label="Save", command=donothing);
        filemenu.add_command(label="Save as", command=donothing);
        filemenu.add_command(label="Import", command=donothing);
        filemenu.add_command(label="Export", command=donothing);
        filemenu.add_separator();
        filemenu.add_command(label="Exit", command=quit);


        #Edit tab on menu bar
        editmenu=Menu(menubar, tearoff=0);
        menubar.add_cascade(label="Edit", menu=editmenu);
        editmenu.add_command(label="Undo", command=donothing);
        #addmenu=Menu(menubar, tearoff=0);
        #menubar.add_cascade(label="Add", menu=addmenu);
        menubar.add_command(label="Add", command=lambda: controller.show_frame(PageOne));


        tk.Label(self, textvariable=fname).grid(column=2, row=3, padx=10, pady=5);
        tk.Label(self, textvariable=lname).grid(column=3, row=3, padx=10, pady=5);
        tk.Label(self, textvariable=address).grid(column=4, row=3, padx=10, pady=5);
        tk.Label(self, textvariable=state).grid(column=5, row=3, padx=10, pady=5);
        tk.Label(self, textvariable=zipC).grid(column=6, row=3, padx=10, pady=5);
        tk.Label(self, textvariable=email).grid(column=7, row=3, padx=10, pady=5);
        tk.Label(self, textvariable=phone_number).grid(column=8, row=3, padx=10, pady=5);


        #Sort by meu
        sort_label=ttk.Label(self, text="Sort by:");
        sort_label.grid(row=0, column=6, stick="e");
        var = StringVar(self);
        options = ["Name", "Zip"];
        var.set(options[0]);
        dropdown = ttk.OptionMenu(self, var, options[0], *options);
        dropdown.grid(row=0, column=7, sticky="w");

        
        t = SimpleTable(self);
        t.grid(row=1, column=0, columnspan=8, padx=20);
        t.print_contacts(contacts);


        


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
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
        tk.Label(self, text="State").grid(column=3, row=6, sticky=(W, E))
        st=ttk.Entry(self, width=7, textvariable=state);
        st.grid(column=3, row=7, sticky=(W, E));
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


        #Bind Enter to create customer as well.

        ttk.Button(self, text="submit", command=lambda: self.add_contact(first_name.get(), last_name.get(), address.get(), state.get(), zipC.get(), em.get(), phone.get())).grid(column=2, row=12);
        ttk.Button(self, text="cancle", command=lambda: controller.show_frame(StartPage)).grid(column=3, row=12);

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5);



    def add_contact(self, fname, lname, address, state, zipC, email, phone):
        #
        #entry = AddressBookEntry("John", "Doe", "123 Daywood Drive", "Portland, MN", "04101", "john@gmail.com")
        #new_contact=[fname, lname, address, state, zipC, email, phone];
        #print(new_contact);
        #
        new_contact=AddressBookEntry(fname, lname, address, state, zipC, email); 
        book.addEntry(new_contact);
        self.controller.refresh_frame(StartPage);
        self.controller.show_frame(StartPage);
        book.exportToFile("SavedAddressBook.txt")
        #self.parent.contacts.append(contact);
        #self.controller.show_frame(StartPage);





def main():
    app=KabyAddrapp();
    app.mainloop();


if __name__ == "__main__":
    main()



