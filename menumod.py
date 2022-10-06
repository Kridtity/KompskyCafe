#Author: Kridtity Ikhlaas Lawang
#Program Name: menumod

#License: GNU GPLv3.0
#Status: Complete
#Version: 1.0
#Release Date: 10-05-2022
#Description: Module for restaurant menu ordering system for Kompsky Cafe

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

#Import modules
import re

#Initialise lists
barbeque_feast_items = ["RUMP STEAK", "PEPPER STEAK", "FINGER RIBS", "CHICKEN WINGS", "HONEY LAMB", "CHILI CHICKEN", "POTATO SALAD", "CREAMY PENNE PASTA", "VEGETARIAN LASAGNE", "BARBECUED PINEAPPLE", "CHEESE BREAD", "GARLIC STEAK", "BEEF RIBS", "LAMB CHUMP", "PARMESAN CHICKEN", "CHICKEN HEARTS", "WHITE RICE", "TOMATO & ONION SALAD", "TOMATO AND ONION SALAD", "MIXED VEGETABLES SALAD", "GARLIC SPAGHETTI", "MASHED POTATOES", "GARLIC BREAD", "SHOESTRING FRIES"]
a_la_carte_items = ["ROCKET SALAD", "GRILLED CHICKEN", "MUSHROOM RISOTTO", "QUESADILLAS", "RAVIOLI"]
a_la_carte_desc = ["Ricotta, sundried tomatoes, walnuts, and homemade balsamic vinegar dressing", "Mixed mushrooms, fresh spinach, Parmigiano cheese, cream, and arborio rice", "Mixed capsicums and mushrooms tossed in spicy sauce. Served in a warm tortilla with sour cream, salsa, and side salad", "Spinach and ricotta ravioli folded in creamy 4 cheese sauce"]
a_la_carte_cost = [17.95, 6.5, 25.95, 23.95, 24.95]
a_la_carte_gf = [True, False, True, True, False]
drinks_items = ["SOFT DRINK CAN", "JUICE", "WATER"]
soft_drinks_items = ["PEPSI", "PEPSI MAX", "COCA COLA", "SUNKIST"]
drinks_cost = [4.0, 5.0, 3.5]
menu_items = barbeque_feast_items + a_la_carte_items + drinks_items

#Set constants
BARBEQUE_FEAST_COST = 54.95
INDIVIDUAL_BARBEQUE_FEAST_COST = 15.00
DISCOUNT = 0.95

#Define function to increment quantity list item by number of menu items sold
def increment_quantity_sold(item):
    #Get quantities of items sold from file
    with open('quantity_sold.txt', 'r') as file:
        quantity_list = file.readlines()

    #Format quantities ready for processing
    for quantity in quantity_list:
        quantity = re.sub(r'\n', '', quantity)
        quantity = re.sub(r'\n\n', '\n', quantity)

    #Increment quantities by amount of item sold
    if item in menu_items:
        increment_position = menu_items.index(item)
        quantity_list[increment_position] = str(int(quantity_list[increment_position]) + 1) + "\n"

    #Write to file
    with open('quantity_sold.txt', 'w') as file:
        for quantity in quantity_list:
            file.write(quantity)

#Define function to apply discount
def apply_discount(takeaway, barbeque_feast_cost, a_la_carte_cost, drinks_cost):
    if takeaway == True:
        total_cost = (barbeque_feast_cost + a_la_carte_cost + drinks_cost) * DISCOUNT
    elif takeaway == False:
        total_cost = barbeque_feast_cost + a_la_carte_cost + drinks_cost
    else:
        print("Error in applying discount.")

    return total_cost

#Function to handle the order by determining costs for the total order, hadnle special order requests, and increment quanitities for items sold and save to file
def handle_order(takeaway, order):
    #Define scope of particular variables, not very Pythonic but allows these variables to be accessed by other functions without the fuss of passing local variables as parameters or referring to variables from a list
    global order_barbeque_feast_items
    global order_a_la_carte_items
    global order_a_la_carte_cost
    global order_drinks_items
    global order_drinks_cost
    global total_barbeque_feast_cost
    global total_a_la_carte_cost
    global total_drinks_cost
    global total_cost
    global barbeque_feast_summary

    #Calculate order cost section
    #Initialise lists to sort order items based on type
    order_barbeque_feast_items = []
    order_a_la_carte_items = []
    order_a_la_carte_cost = []
    order_drinks_items = []
    order_drinks_cost = []

    #Initialising here because I can't write a sum operation inside a loop without first defining the initial value of the variable, even thopugh intialising int vars like this is very non-Pythonic
    total_barbeque_feast_cost = 0
    total_a_la_carte_cost = 0
    total_drinks_cost = 0

    #Determine BBQ feast items cost in order and append to new list
    if takeaway == False:        
        for x in order:
            if x in barbeque_feast_items:
                order_barbeque_feast_items.append(x)
                increment_quantity_sold(x)
            else:
                continue
            
        #Calculate Barbeque Feast order items cost based on amount ordered and sets of 4 ordered
        if len(order_barbeque_feast_items) <= 3:
            total_barbeque_feast_cost = INDIVIDUAL_BARBEQUE_FEAST_COST * len(order_barbeque_feast_items)
            barbeque_feast_summary = "{}x individual Barbeque Feast items".format(len(order_barbeque_feast_items))
        elif (len(order_barbeque_feast_items) % 4) == 0:
            multiplier = len(order_barbeque_feast_items) / 4
            total_barbeque_feast_cost = BARBEQUE_FEAST_COST * multiplier
            barbeque_feast_summary = "{}x group Barbeque Feast items".format(multiplier)
        elif len(order_barbeque_feast_items) >= 4:
            individual_multiplier = len(order_barbeque_feast_items) % 4
            group_multiplier = (len(order_barbeque_feast_items) - individual_multiplier) / 4
            total_barbeque_feast_cost = BARBEQUE_FEAST_COST * group_multiplier + INDIVIDUAL_BARBEQUE_FEAST_COST * individual_multiplier
            barbeque_feast_summary = "{:.0f}x group Barbeque Feast items, {:.0f}x individual Barbeque Feast items".format(group_multiplier, individual_multiplier)
        else:
            print("Error calculating BBQ Feast cost.")
    elif takeaway == True:
        pass
    else:
        print("Error in calculating Barbeque Feast details.")

    #Determine A La Carte items cost in order
    for x in order:
        if x in a_la_carte_items:
            order_a_la_carte_cost.append(a_la_carte_cost[a_la_carte_items.index(x)])
            order_a_la_carte_items.append(x)
            total_a_la_carte_cost += float(a_la_carte_cost[a_la_carte_items.index(x)])
            increment_quantity_sold(x)
        else:
            continue
        
    #Determine drinks items cost in order
    for x in order:
        if x in drinks_items:
            order_drinks_cost.append(drinks_cost[drinks_items.index(x)])
            order_drinks_items.append(x)
            total_drinks_cost += float(drinks_cost[drinks_items.index(x)])
            increment_quantity_sold(x)
        else:
            continue

    #Iteration to handle special A La Carte requests and soft drink orders
    for x in order:
        if "-" in x:
            request = x.split("-")
            item_index = order.index(x)
            
            #Handle gluten free requests for eligible items
            if request[0] in a_la_carte_items:
                if "GF" or "GLUTEN FREE" in request and a_la_carte_gf[a_la_carte_items.index(request[0])] == True:
                    order[item_index] = request[0] + " - GLUTEN FREE"
                    order_a_la_carte_cost.append(a_la_carte_cost[a_la_carte_items.index(request[0])])
                    order_a_la_carte_items.append(order[item_index])
                    total_a_la_carte_cost += float(a_la_carte_cost[a_la_carte_items.index(request[0])])
                    increment_quantity_sold(request[0])

                #Non-eligible items have the gluten free request removed
                elif "GF" or "GLUTEN FREE" in request and a_la_carte_gf[a_la_carte_items.index(request[0] == False)]:
                    order[item_index] = request[0]
                else:
                    continue
                
                #Handle grilled chicken for eligible item
                if "ADD GRILLED CHICKEN" or "GRILLED CHICKEN" in request and request[0] == "ROCKET SALAD":
                    order[item_index] += " - ADD GRILLED CHICKEN"
                    order.insert(item_index + 1, "GRILLED CHICKEN")
                    order_a_la_carte_cost.append(a_la_carte_cost[a_la_carte_items.index("GRILLED CHICKEN")])
                    order_a_la_carte_items[-1] = order[item_index]
                    order_a_la_carte_items.append("GRILLED CHICKEN")
                    total_a_la_carte_cost += float(a_la_carte_cost[a_la_carte_items.index(request[0])])
                    increment_quantity_sold("GRILLED CHICKEN")

                #Non-eligible items have the grilled chicken request removed
                elif "ADD GRILLED CHICKEN" or "GRILLED CHICKEN" in request and request[0] != "ROCKET SALAD":
                    order[item_index] = request[0]
                else:
                    continue
            
            #Handle softdrink can type requests, if type is not in list ignore and list only as soft drink can
            if request[0] in drinks_items:
                if "SOFT DRINK CAN" in request and request[1] in soft_drinks_items:
                    order[item_index] = request[0] + " - " + request[1]
                    order_drinks_cost.append(drinks_cost[drinks_items.index(request[0])])
                    order_drinks_items.append(order[item_index])
                    total_drinks_cost += float(drinks_cost[drinks_items.index(request[0])])
                    increment_quantity_sold(request[0])
                elif "SOFT DRINK CAN" in request and request[1] not in soft_drinks_items:
                    order[item_index] = request[0]
                    order_drinks_cost.append(drinks_cost[drinks_items.index(request[0])])
                    order_drinks_items.append(order[item_index])
                    total_drinks_cost += float(drinks_cost[drinks_items.index(request[0])])
                    increment_quantity_sold(request[0])
                else:
                    continue

    #Determine total cost of order
    total_cost = apply_discount(takeaway, total_barbeque_feast_cost, total_a_la_carte_cost, total_drinks_cost)

    #Write total cost of order into the 'order_totals.txt' file
    with open('order_totals.txt', 'a') as file:
        file.write(str(total_cost) + "\n")
                
#Run total order cost function and summarise order in a Shell/command line output and print to a text file total order cost
def total_order_cost_and_summaries(customer_name, order, takeaway_choice, takeaway):
    #Process order costs and organise into categories
    handle_order(takeaway, order)
    
    #Define function to print order summary to Shell/text file   
    #Print order summary to Shell
    print("----------------------------------\n"
          "|          Order Summary         |\n"
          "----------------------------------\n"
          "Customer name: {}\n"
          "Dining choice: {}\n".format(customer_name, takeaway_choice))
    if takeaway == False:
        print("Barbeque Feast:")
        for x in order_barbeque_feast_items:
            x.capitalize()
            print("{}".format(x))
        print(barbeque_feast_summary)
        print("                             ${:.2f}".format(total_barbeque_feast_cost))
        print("")
    print("A La Carte:")
    for x in order_a_la_carte_items:
        x.capitalize()
        print("{}".format(x))
        print("                             ${:.2f}".format(order_a_la_carte_cost[order_a_la_carte_items.index(x)]))
    print("")
    print("Drinks:")
    for x in order_drinks_items:
        x.capitalize()
        print("{}".format(x))
        print("                             ${:.2f}".format(order_drinks_cost[order_drinks_items.index(x)]))
    print("")
    print(""
          "Total cost:                  ${:.2f}".format(total_cost))

    #Print order summary to text file
    with open('order.txt', 'w') as file:
        file.write("----------------------------------\n"
                   "|          Order Summary         |\n"
                   "----------------------------------\n"
                   "Customer name: {}\n"
                   "Dining choice: {}\n\n".format(customer_name, takeaway_choice))
        if takeaway == False:
            file.write("Barbeque Feast:\n")
            for x in order_barbeque_feast_items:
                x.capitalize()
                file.write("{}\n".format(x))
            file.write(barbeque_feast_summary)
            file.write("\n"
                       "                             ${:.2f}\n\n".format(total_barbeque_feast_cost))
        file.write("A La Carte:\n")
        for x in order_a_la_carte_items:
            x.capitalize()
            file.write("{}\n".format(x))
            file.write("                             ${:.2f}\n".format(order_a_la_carte_cost[order_a_la_carte_items.index(x)]))
        file.write("\n")
        file.write("Drinks:\n")
        for x in order_drinks_items:
            x.capitalize()
            file.write("{}\n".format(x))
            file.write("                             ${:.2f}\n".format(order_drinks_cost[order_drinks_items.index(x)]))
        file.write("\n")
        file.write("Total cost:                  ${:.2f}".format(total_cost))