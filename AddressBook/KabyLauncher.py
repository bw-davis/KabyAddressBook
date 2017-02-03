"""
Module used to start the kabby address book application.
"""

from Frames import *


"""
Function that executes when the KabyLauncer.py file is executed. This creates the first KabyAddrapp instances.
"""
def main():
    lastbook = get_last_book();


    app = KabyAddrapp(lastbook);
    app.protocol("WM_DELETE_WINDOW", lambda: on_closing(app));
    starttime = datetime.datetime.now()

    app.mainloop();
    #set_last_book(lastbook);
    endtime = datetime.datetime.now()

"""
Executes main function when this file is executed.
"""
if __name__ == "__main__":
    main() 
