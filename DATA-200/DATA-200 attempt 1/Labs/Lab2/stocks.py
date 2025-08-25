# Summary: This module is just a shorter name for the program that can start either the Console or GUI version of the program.

import stock_console
import stock_GUI

def main():
    #For Console Version
    #stock_console.main()

    #For GUI Version
    stock_GUI.main()
    return

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a script
    main()