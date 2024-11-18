import psycopg2
from random import randint


conn = psycopg2.connect(database = "ecommerce", 
                        user = "postgres", 
                        host= 'localhost',
                        password = "12345678",
                        port = 5432)



# Open a cursor to perform database operations
for i in range(2995):
    shuffle = randint(0, 9)
    product_name = ['Mobile', 'Charger', 'Handfree', 'Laptop', 'Chess', 'Ball', 'Tie', 'Shoe', 'Watch', 'Goggles'][shuffle]
    if shuffle > 5:
        category = 'Fashion'
    elif shuffle > 3:
        category = 'Toys'
    else:
        category = 'Electronics'
    
    shuffle = randint(0, 9)
    price = [6000.5, 700.5, 500, 550.5, 120, 950, 1050.5, 2500, 5000, 1000][shuffle]
    shuffle = randint(0, 9)
    quantity = [50, 100, 25, 60, 10, 15, 200, 30, 45, 90][shuffle]


    cur = conn.cursor()

    cur.execute(
        'INSERT INTO public.shop_app_product (product_name, category, price, quantity) VALUES (%s, %s, %s, %s)',
        (product_name, category, price, quantity)
    )


    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()


conn.close()

# print("Successfull")