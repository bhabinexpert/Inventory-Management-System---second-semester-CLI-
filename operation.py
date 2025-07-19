import write
import read
from datetime import datetime

def sell_product():
    """
    Handles the purchase of products by a customer, updating stock and generating an invoice.

    The function prompts for the customer's name and product details, checks stock availability,
    applies a bonus (1 extra item per 3 purchased), updates the stock, calculates VAT (13% of total cost),
    and generates an invoice for all purchased products when the customer chooses to stop buying.
    Costs and VAT are handled as floats with two decimal places. The invoice includes total amount,
    total VAT, and total amount including VAT.

    Arguments:
        None

    Returns:
        None
    """
    with open("info.txt", "r") as file:
        product = file.read() 
        list = product.strip().split("\n")
        newlist = []
        for i in range(len(list)):
            newlist.append(list[i].split(', '))  # Splitting each line into list of strings

    # Get buyer's name
    customer_name = input("Enter the customer's name: ")
    

    # List to hold purchased products
    purchased_products = []

    while True:
        # Get product details
        product_to_sell = input("Enter the product you want to sell: ")
        

        # Check if the product exists in the stock
        product_found = False
        vendor_name = ''
        for i in newlist:
            if i[0].lower() == product_to_sell.lower():
                vendor_name = i[1]  # Get the vendor name from the info.txt if it's an existing product
                product_found = True
                break

        if not product_found:
            print("Error: " + product_to_sell + " is not available in the stock!")
            more = input("Do you want to sell more products? (yes/no): ")
            while more.lower() not in ['yes', 'no']:
                print("Invalid input! Please enter 'yes' or 'no'.")
                more = input("Do you want to sell more products? (yes/no): ")
           
            if more.lower() == 'no':
                return  # Exit to the main menu
            continue  # Ask for product name again

        # If product is found, proceed with quantity
        while True:
            try:
                quantity_to_sell = int(input("Enter the quantity you want to sell: "))
                if quantity_to_sell <= 0:
                    print("Quantity should be a positive integer greater than zero. Please try again.")
                    continue
                break  # Exit the loop if valid input
            except ValueError:
                print("Invalid input! Please enter a valid number for quantity.")

        # Get the product stock details
        total_cost = 0.0
        bonus_items = 0
        for i in newlist:
            if i[0].lower() == product_to_sell.lower():
                current_qty = int(i[2])
                product_price = float(i[3])  # Read as float

                # Check if the user wants more products than are available
                if quantity_to_sell > current_qty:
                    print("Error: Only " + str(current_qty) + " " + product_to_sell + "(s) are available in stock.")
                    continue  # Ask the user to try again

                # Apply bonus logic: 1 bonus item per 3 items bought
                bonus_items = (quantity_to_sell // 3)
                

                # Check if bonus quantity + quantity_to_buy exceeds available stock
                if quantity_to_sell + bonus_items > current_qty:
                    print("Error: The total quantity you want to buy (including bonuses) exceeds available stock.")
                    continue  # Ask the user to try again

                # Deduct purchased quantity (including bonus) from the stock
                i[2] = str(current_qty - quantity_to_sell - bonus_items)
                

                total_cost = product_price * quantity_to_sell
               
                # Calculate VAT (13% of total cost)
                vat = total_cost * 0.13
               

                # Add the product to the list of purchased products
                purchased_products.append({
                    "product_name": i[0],
                    "quantity": quantity_to_sell,
                    "bonus": bonus_items,
                    "total_cost": total_cost,
                    "vat": vat,
                    "vendor_name": vendor_name
                })
                break  # Exit loop once the product is found and processed

        # Ask if the customer wants to buy more products
        more = input("Do you want to sell more products? (yes/no): ")
        while more.lower() not in ['yes', 'no']:
            print("Invalid input! Please enter 'yes' or 'no'.")
            more = input("Do you want to sell more products? (yes/no): ")
        if more.lower() == 'no':
            # Display "Generating Invoice..."
            print("\nGenerating Invoice...\n")
            print("Customer Name: " + customer_name + "\n")

            # Display purchased products details
            total_amount = 0.0
            total_vat = 0.0
            for product in purchased_products:
                print("Product: " + product['product_name'])
                print("Quantity: " + str(product['quantity']) + " | Bonus: " + str(product['bonus']))
                print("Vendor Name: " + product['vendor_name'])
                print(f"Total Cost: RS: {product['total_cost']:.2f}")
                print(f"VAT (13%): RS: {product['vat']:.2f}\n")

                total_amount = total_amount + product['total_cost']
                total_vat = total_vat + product['vat']

            print(f"Total Amount: Rs: {total_amount:.2f}")
            print(f"Total VAT: Rs: {total_vat:.2f}")
            print(f"Total Amount Including VAT: Rs: {(total_amount + total_vat):.2f}\n")


            # Get current timestamp
            c_time = datetime.now()
            timestamp = str(c_time.year) + "_" + str(c_time.month) + "_" + str(c_time.day) + "_" + str(c_time.hour) + "_" + str(c_time.minute) + "_" + str(c_time.second)
            
            invoice_filename = timestamp + "_" + customer_name + "-invoice.txt"
            
            write.generate_invoice(customer_name, purchased_products, invoice_filename)
            
            write.update_product_stock(newlist)  # Update stock after all purchases
            
            break  # Exit the loop to stop purchasing

def restock_product():
    """
    Handles restocking of existing or new products, updating stock and generating a restock invoice.

    The function allows the admin to restock multiple products (existing or new) in one session,
    prompting after each restock to continue. It updates the stock in memory, calculates VAT (13% of total cost),
    generates a single restock invoice when the admin chooses to stop, and updates the info.txt file.
    The invoice format matches the purchase invoice generated by buy_product. Costs and VAT are handled as floats.
    The invoice includes total amount, total VAT, and total amount including VAT.

    Arguments:
        None

    Returns:
        None
    """
    try:
        with open("info.txt", "r") as file:
            product_data = file.read().strip().split("\n")
            product_list = [line.split(', ') for line in product_data]
        
    except FileNotFoundError:
        print("Error: The 'info.txt' file is missing.")
        return
    except Exception as e:
        print("Error reading file: " + str(e))
        return

    # List to hold restocked products
    restocked_products = []

    while True:
        # Ask admin whether they want to restock a new or existing product
        restock_choice = input("\nDo you want to restock an existing product or a new product? (existing/new): ").strip().lower()
      

        while restock_choice not in ['existing', 'new']:
            print("Invalid option! Please choose 'existing' or 'new'.")
            restock_choice = input("\nDo you want to restock an existing product or a new product? (existing/new): ").strip().lower()

        if restock_choice == 'existing':
            product_found = False
            while not product_found:
                restock_choice_existing = input("\nEnter the product you want to Restock: ").strip()
                
                for i in product_list:
                    if i[0].lower() == restock_choice_existing.lower():
                        product_found = True
                        current_qty = int(i[2])
                        cost = float(i[3])  # Read as float
                        vendor_name = i[1]
                        

                        # Ask for the quantity to restock
                        while True:
                            try:
                                adding_qty = int(input("Enter the quantity of " + restock_choice_existing + " you want to restock: "))
                                if adding_qty <= 0:
                                    print("Quantity should be a positive integer greater than zero. Please try again.")
                                    continue
                                break
                            except ValueError:
                                print("Invalid input! Please enter a valid number for quantity.")

                        # Update the product quantity 
                        i[2] = str(current_qty + adding_qty)
                       

                        # Calculate total cost and VAT
                        total_cost = cost * adding_qty
                       
                        vat = total_cost * 0.13
                        

                        # Add to restocked products list
                        restocked_products.append({
                            "product_name": i[0],
                            "quantity": adding_qty,
                            "bonus": 0,  # No bonus for restocking
                            "total_cost": total_cost,
                            "vat": vat,
                            "vendor_name": vendor_name
                        })
                        

                        print("\n" + restock_choice_existing + " has been restocked with " + str(adding_qty) + " units!")
                        break

                if not product_found:
                    print(restock_choice_existing + " is not found in the stock! Please enter a valid product.")

        elif restock_choice == 'new':
            # Collect information for the new product
            print("\nEnter the details of the new product:")
            name = input("Enter the product name: ")
            
            vendor_name = input("Enter the vendor's name: ")
           

            while True:
                try:
                    quantity = int(input("Enter the initial stock quantity: "))
                    if quantity <= 0:
                        print("Quantity should be a positive integer greater than zero. Please try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid input! Please enter a valid number for quantity.")

            while True:
                try:
                    cost = float(input("Enter the cost of the product: "))
                    if cost <= 0:
                        print("Cost should be a positive number. Please try again.")
                        continue
                    break
                except ValueError:
                    print("Invalid input! Please enter a valid number for cost.")

            country = input("Enter the country of manufacture: ")

            # Calculate total cost and VAT
            total_cost = cost * quantity
            print(f"\nTotal cost calculated: RS: {total_cost:.2f}")

            vat = total_cost * 0.13
            print(f"VAT calculated (13%): RS: {vat:.2f}")

            # Add the new product to the list
            new_product = [name, vendor_name, str(quantity), str(round(cost, 2)), country]
            product_list.append(new_product)
            

            # Add to restocked products list
            restocked_products.append({
                "product_name": name,
                "quantity": quantity,
                "bonus": 0,  # No bonus for restocking
                "total_cost": total_cost,
                "vat": vat,
                "vendor_name": vendor_name
            })
            

            print("New product " + name + " added to the stock successfully!")

        # Ask if the admin wants to restock more products
        more = input("\nDo you want to restock more products? (yes/no): ").strip().lower()
        while more not in ['yes', 'no']:
            print("Invalid input! Please enter 'yes' or 'no'.")
            more = input("Do you want to restock more products? (yes/no): ").strip().lower()
       

        if more == 'no':
            if restocked_products:
                # Get current timestamp
                c_time = datetime.now()
                timestamp = str(c_time.year) + "_" + str(c_time.month) + "_" + str(c_time.day) + "_" + str(c_time.hour) + "_" + str(c_time.minute) + "_" + str(c_time.second)
                
                invoice_filename = timestamp + "_restock-invoice.txt"
                
                # Modified invoice generation without "Restocked by: Admin"
                shop_name = "WE CARE SKIN PRODUCTS"
                invoice_content = shop_name + "\n"
                invoice_content = invoice_content + "Timestamp: " + timestamp + "\n"
                invoice_content = invoice_content + "=" * 30 + "\n"
                
                total_amount = 0.0
                total_vat = 0.0

                for product in restocked_products:
                    product_name = product["product_name"]
                    quantity = product["quantity"]
                    total_cost = product["total_cost"]
                    vat = product["vat"]
                    vendor_name = product["vendor_name"]

                    invoice_content = invoice_content + "Product: " + product_name + "\n"
                    invoice_content = invoice_content + "Quantity: " + str(quantity) + "\n"
                    invoice_content = invoice_content + "Vendor Name: " + vendor_name + "\n"
                    invoice_content += f"Total Cost: RS: {total_cost:.2f}\n"
                    invoice_content += f"VAT (13%): RS: {vat:.2f}\n"

                    invoice_content = invoice_content + "=" * 30 + "\n"

                    total_amount = total_amount + total_cost
                    total_vat = total_vat + vat
                    
                invoice_content = invoice_content + f"Total Amount: Rs: {total_amount:.2f}\n"
                invoice_content = invoice_content + f"Total VAT: Rs: {total_vat:.2f}\n"
                invoice_content = invoice_content + f"Total Amount Including VAT: Rs: {(total_amount + total_vat):.2f}\n"
                invoice_content = invoice_content + "=" * 30 + "\n"

                # Save the invoice to the specified file
                try:
                    with open(invoice_filename, "w") as file:
                        file.write(invoice_content)
                    print("\n" + "Restock invoice saved to: " + invoice_filename)
                except Exception as e:
                    print("Error saving restock invoice: " + str(e))
                    return

                # Display restock invoice
                print("\nRestock Invoice Generated...")
                print(invoice_content)

                # Update the product stock in the file
                try:
                    write.update_product_stock(product_list)
                    
                except Exception as e:
                    print("Error updating stock: " + str(e))
                    return
            else:
                print("No products were restocked.")
            
            break