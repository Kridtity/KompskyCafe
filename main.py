#Author: Kridtity Ikhlaas Lawang
#Program Name: Kompsky Cafe Restaurant Ordering System

#License: GNU GPLv3.0
#Status: Complete
#Version: 1.0
#Release Date: 10-05-2022
#Description: Menu ordering system for Kompsky Cafe

#Copyright (C) 2022 Kridtity Lawang

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.

#NOTE: THE TERMS ARRAY AND LIST ARE USED INTERCHANGEABLY IN THIS PROGRAM IS REFERENCE TO PYTHON LISTS.

#Import modules (menumod is self-created)
import menumod
import re
import webbrowser
import importlib
import main
import os

#Initialises array to contain customer order
order = []

#Define function to prevent program from closing immediately after finishing running previous code sequence by waiting for random input (i.e. wait until key pressed to close program), or by giving the user an option to return to the main menu
def wait_to_close():
    print("")
    i = input("Enter R to reload or any other key to quit: ").upper()
    
    if i == "R":
        importlib.reload(main)
    else:
        quit()

#Main code begins
#Print intro and main menu choices
print("----------------------------------\n"
      "| Kompsky Cafe Menu Order System | \n"
      "----------------------------------\n")

menu_select = input("----------------------------------\n"
                    "|           Main  Menu           |\n"
                    "----------------------------------\n"
                    "Enter: I -> Input customer order\n"
                    "       P -> Print last customer order into the Shell/command line\n"
                    "       M -> Print menu into the Shell/command line\n"
                    "       S -> Print day summary\n"
                    "       R -> Reset day summary\n"
                    "       H -> Help manual\n"
                    "       E -> Exit the program\n").upper()

#Following selection stuctrue based on menu_select input, invalid selections are prompted to restart or quit
#Following menu_select is the main part of the program and handles new orders
if menu_select == "I":
    #Print basic use instructions and input options, customer name input received first
    customer_name = input("----------------------------------\n"
                          "|      Input customer order      |\n"
                          "----------------------------------\n"
                          "Enter customer name: ").upper()

    #Print dine-in/takeaway options
    takeaway_choice = input("Dine-in or takeaway? ").capitalize()
    
    #Set takeaway boolean to be used in menumod module for discount calculations and menu options, invalid selections are prompted to restart or quit
    if takeaway_choice == "Takeaway":
        takeaway = True
    elif takeaway_choice == "Dine-in":
        takeaway = False
    else:
        print("Please enter a valid input.\n")
        wait_to_close()
    
    #Receive order inputs section and print ready to receive input notice
    print("Enter customer order items seperated by a new line\n"
          "  then enter \"DONE\" to finalise order")
    
    #Initialise new_order_item array so while loop can check conditon
    new_order_item = ""

    #Receive order items and store in array
    while new_order_item != "DONE":
        new_order_item = input("").upper()

        order.append(new_order_item)
    else:
        order.remove("DONE")
        print("\n------------------------------\n")

    #Pre-made order array for testing purposes
    #IGNORE IF NOT DEBUGGING
    #order = ['RUMP STEAK', 'LAMB CHUMP', 'MASHED POTATOES', 'GARLIC BREAD', 'ROCKET SALAD-GF-GRILLED CHICKEN', 'SOFT DRINK CAN-PEPSI']

    #Run function from module to process order and prompt user to restart or quit once invoice is displayed on screen and saved to file (functionality in module except for quitting and restarting protocol)
    menumod.total_order_cost_and_summaries(customer_name, order, takeaway_choice, takeaway)
    wait_to_close()

##Following menu_select prints the previous order or an error message is no previous order information is available
elif menu_select == "P":
    try:
        #Writes file contents to array
        with open('order.txt', 'r') as file:
            file_lines = file.readlines()

        #Format file lines in array and print
        for line in file_lines:
            file_lines[file_lines.index(line)] = line.strip()
            
            print(line)
            
    #Exception to handle case where there is no 'order.txt' storing previous order information
    except Exception as e:
        print(e)
        print("\nThere is either no file named 'order.txt' or previous order made or both.")
    
    #Prompt user to restart program or quit
    wait_to_close()

#Following menu_select prints the menu
elif menu_select == "M":
    try:
        #Writes file contents to array
        with open('menu.txt', 'r') as file:
            file_lines = file.readlines()

        #For the lines in the array, format each line and print it to the Shell/command line
        for line in file_lines:
            line = re.sub(r'\n', '', line)
            line = re.sub(r'\n\n', '\n', line)
                
            print(line)

    #Exception to handle case where there is no 'menu.txt' storing menu information
    except Exception as e:
        print(e)
        print("\nThere is no file named 'menu.txt'. Contact the developer team or re-download the source code to obtain 'menu.txt'.")
    
    #Prompt user to restart program or quit
    wait_to_close()

#Following menu_select prints the day summary
elif menu_select == "S":
    #Open menu items and quantity files and append to arrays, then format
    with open('menu_items.txt', 'r') as file:
        menu = file.readlines()

    for item in menu:
        menu[menu.index(item)] = item.strip()

    with open('quantity_sold.txt', 'r') as file:
        quantity = file.readlines()

    for number in quantity:
        quantity[quantity.index(number)] = number.strip()

    #Determine total turnover by reading file lines of previously stored order totals, the getting the sum of all values
    with open('order_totals.txt', 'r') as file:
        totals = file.readlines()

        for x in totals:
            totals[totals.index(x)] = float(x)

    total_turnover = sum(totals)

    #Print summary info or menu item, qauntity of the item sold, and the total day's turnover
    print("Day Summary:")
    for x in menu:
        print("{}x {}\n".format(quantity[menu.index(x)], x))

    print("Total Day Turnover: ${:.2f}\n".format(total_turnover))

    #Prompt user to restart program or quit
    wait_to_close()

#Following menu_select resets the day summary, quantities sold, and deletes the 'order.txt' and 'order_totals.txt' files
elif menu_select == "R":
    with open('quantity_sold.txt', 'w') as file:
        for x in range(0, 32):
            file.write("0\n")

    try:
        os.remove('order.txt')
        os.remove('order_totals.txt')
        
    except:
        pass
    
    print("Day summary reset.")

    #Prompt user to restart program or quit
    wait_to_close()

##Following menu_select prints the help instructions and user manual
elif menu_select == "H":
    print("----------------------------------\n"
          "|           Help Manual          |\n"
          "----------------------------------\n")

    print("Assumptions:\n"
          "1. The BBQ Feast cost for four items (one full set) is $54.95. Each individual dish costs $15.00.\n"
          "Any combination of BBQ Feast sishes may be made, with each set of four being discounted and each other dish costing $15.00.\n\n\n\n" 
          "Basic Use:\n"
          "From the main menu, enter:\n"
          "I -> Input customer order\n"
          "     This option receives continuous inputs of one item at a time for a single customer order\n"
          "     until the keyword \"DONE\" is entered. Seperate special requests for orders such by entering\n"
          "     the order in the following format: ITEM-SPECIAL_REQUEST_1-SPECIAL_REQUEST_2\n"
          "     (i.e. item followed by special requests seperated by hyphens.\n"
          "     (Note: special requests only include gluten free/gf, grilled chicken, and soft drink orders)\n"
          "     \n"
          "     Examples: rocket salad-gf-grilled chicken\n"
          "               quesadillas-gf\n"
          "               soft drink can - pepsi max\n"
          "     \n"
          "     IMPORTANT: INVALID SPECIAL REQUESTS WILL BE IGNORED!\n\n\n"
          "P -> Print last customer order into the Shell/command line\n"
          "     This option prints the last stored order made in the program.\n\n\n"
          "M -> Print menu into the Shell/command line\n"
          "     This option prints the entire menu and corresponding prices for Kompsky Cafe into the Shell.\n\n\n"
          "S -> Print day summary\n"
          "     This option prints the total quantity of each menu item sold for each item and the total revenue\n"
          "     received by the cafe for the day (i.e. since the last reset).\n\n\n"
          "R -> Reset day summary\n"
          "     This option resets all quantities sold and revenue amounts to 0. Deletes the last customer order stored.\n\n\n"
          "H -> Help manual\n"
          "     This option displays prints the help manual to the SHell/command line (i.e. this page).\n\n\n"
          "E -> Exit the program\n"
          "     This option quits the program.")

    #Prompt user to restart program or quit
    wait_to_close()

#Following menu_select quits the program
elif menu_select == "E":
    quit()

#Following menu_select is not part of the main menu and exists as a hidden option to trigger a rickroll
elif menu_select == "42":
        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

        #Prompt user to restart program or quit
        wait_to_close()

#Following menu_select is not part of the main menu and exists as a hidden option to trigger an immediate shutdown on the Windows machine
elif menu_select == "69":
        os.system(r'shutdown /s /d u:5:15 /f /t 10 /c "Bonk, no horny. By the way, you have 10 seconds before your computer shuts down. Sucks to be you lol"')

#Following menu_select is not part of the main menu and exists as a hidden option to trigger an immediate shutdown on the Windows machine
elif menu_select == "420":
        os.system(r'shutdown /s /d u:5:15 /f /t 0 /c "Get wrecked."')

#Handle invalid menu_select inputs
else:
    print("Please enter a valid input.\n")

    #Prompt user to restart program or quit
    wait_to_close()