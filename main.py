import read
import operation
"""
Main menu for the WE CARE SKIN PRODUCTS application.

This is the central interface users interacts with. It displays options to:
1. View available products
2. Sell products (customer purchase)
3. Restock items (admin adds product)
4. Exit the program

Functions used:
- check_int_validation(num): Ensures the user's input is a positive integer.
- read.display(): From read.py, it shows all products in stock.
- operation.sell_product(): From operation.py, handles customer purchase.
- operation.restock_product(): From operation.py, handles restocking items.

Loop:
The menu runs in a loop until the user selects '4' to exit.
Each action is followed by re-displaying the main menu.
"""

def check_int_validation(num):
    """
    Validates whether the given input is a positive integer greater than zero.

    Arguments:
        num (str): The input provided by the user as a string.

    Returns:
        boolean
            - True if the input is a valid positive integer greater than zero.
            - False if the input is not a valid integer or is less than or equal to zero.
    """

    try:
        num = int(num)
        if num <= 0:
            print("!!! Please enter a positive integer greater than zero.")
            return False
        return True
    except:
        print("!!! Invalid input.. Please enter a valid integer.")
        return False

def bordermain(): 
    while True:
        def bordertop():
            for i in range(30):
                print("=", end="")
            print()
        bordertop()

        # Display the Welcome Message and Options
        print("\n \t Welcome!!!\n")
        print("*** WE CARE SKIN PRODUCTS ***\n")
        print("Choose any Option between (1-4) for your choice of action:")
        print("1. View Products")
        print("2. Sell Products")
        print("3. Restock Items")
        print("4. Exit")
        
        def borderbuttom():
            for i in range(30):
                print("=", end="")
            print()
        borderbuttom()

        # Prompt user for input
        print("\n")
        user_input = input("Enter the number according to your choice of action as stated above: ")
        value = check_int_validation(user_input)

        if value == True:
            if user_input in ['1', '2', '3', '4']:
                if user_input == '1':
                    read.display()  # Display the products from read.py
                
                elif user_input == '2':
                    operation.sell_product()  # Call buy_product() function from operation.py
                
                elif user_input == '3':
                    operation.restock_product()  # Call restock_product() function from operation.py
                
                elif user_input == '4':
                    print("\nThank you for Shopping with us!! Have a Good Day!! \n")
                    break
            else:
                print("!!!Please enter a number between 1-4 according to your choice of action as stated above:")

# Start the main program
bordermain()