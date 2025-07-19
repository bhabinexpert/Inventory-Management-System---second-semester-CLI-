def display():
    """
    Displays the available products from the 'info.txt' file in a formatted table.

    This function reads product data from 'info.txt', processes it into a structured format,
    and prints a table containing product name, vendor name, available quantity, calculated cost
    (multiplied by 2), and manufacturing country.

    Arguments:
        None

    Returns:
        None

    """
    try:
        with open("info.txt", "r") as file:
            product = file.read() 
            list = product.strip().split("\n")
         
            newlist = []
            for i in range(len(list)):
                newlist.append(list[i].split(', '))
               
            print("\nAvailable Products:\n")
            print("----" * 31)
            print(f"{'| Name of the Product:':<20} | {"Vendor's Name":<30} | {'Available Quantity':<25} | {'Cost':<10} | {'Manufacturing Country   |':<22}")
            print("----" * 31)
            for i in newlist:
                print(f"| {i[0]:<20} | {i[1]:30} | {i[2]:<25} | {float(i[3]) * float(2):<10} | {i[4]:<22}  |")
                print("----" * 31)
        print("\n")
    except FileNotFoundError:
        print("The file is not found..Please Make sure the file exists!!")

      
