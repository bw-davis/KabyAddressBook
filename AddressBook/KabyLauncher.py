"""
This module containes the KabyAddrapp class, when this class is executed a KabyAddrapp instance is created and
the last edited address book.
"""

from Frames import *
#from DisplayContacts import *






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
