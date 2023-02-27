import mysql.connector

# establish database connection
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="toorpassword",
  database="whatabook"
)

# initialize cursor
cursor = db.cursor()

# function to display main menu
def display_main_menu():
    print("\nWelcome to WhatABook!")
    print("1. View Books")
    print("2. View Store Locations")
    print("3. My Account")
    print("4. Exit")
    
# function to display account menu
def display_account_menu():
    print("\nMy Account")
    print("1. Wishlist")
    print("2. Add Book to Wishlist")
    print("3. Main Menu")
    
# function to display list of available books
def display_books():
    query = "SELECT * FROM book"
    cursor.execute(query)
    books = cursor.fetchall()
    print("\nList of Available Books:")
    for book in books:
        print("ID:", book[0])
        print("Title:", book[1])
        print("Author:", book[2])
        print("Details:", book[3])
        print()
        
# function to display list of store locations
def display_store_locations():
    query = "SELECT * FROM store"
    cursor.execute(query)
    store = cursor.fetchall()
    print("\nList of Store Locations:")
    for location in store:
        print(location[0], "-", location[1])
    print()
    
# function to display user's wishlist
def display_wishlist(user_id):
    query = "SELECT book_id FROM wishlist WHERE user_id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    wishlist = cursor.fetchall()
    if wishlist:
        print("\nYour Wishlist:")
        for book in wishlist:
            query = "SELECT * FROM book WHERE book_id = %s"
            values = (book[0],)
            cursor.execute(query, values)
            book_details = cursor.fetchone()
            print("ID:", book_details[0])
            print("Title:", book_details[1])
            print("Author:", book_details[2])
            print("Details:", book_details[3])
            print()
    else:
        print("\nYour Wishlist is empty.\n")
    
# function to add book to user's wishlist
def add_to_wishlist(user_id):
    display_books()
    book_id = int(input("Enter the ID of the book you would like to add to your wishlist: "))
    query = "INSERT INTO wishlist (user_id, book_id) VALUES (%s, %s)"
    values = (user_id, book_id)
    cursor.execute(query, values)
    db.commit()
    print("Book added to wishlist.\n")

# main program loop
while True:
    display_main_menu()
    choice = input("Enter a choice (1-4): ")
    if choice == "1":
        display_books()
    elif choice == "2":
        display_store_locations()
    elif choice == "3":
        user_id = input("Enter your user ID: ")
        query = "SELECT * FROM user WHERE user_id = %s"
        values = (user_id,)
        cursor.execute(query, values)
        user = cursor.fetchone()
        if user:
            display_account_menu()
            choice = input("Enter a choice (1-3): ")
            if choice == "1":
                display_wishlist(user_id)
            elif choice == "2":
                add_to_wishlist(user_id)
            elif choice == "3":
                continue
            else:
                print("Invalid choice. Please try again.")
        else:
            print("Invalid user ID. Please try again.")
