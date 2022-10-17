from ast import keyword
from multiprocessing.sharedctypes import Value
from optparse import Values
import sqlite3
from traceback import print_tb
from unicodedata import name
from venv import create
from warnings import catch_warnings


def get_table_choice(x):
    # table_choice is used to decide the table we are working with and
    # is used in conjunction with f strings to adapt the
    # select statement passed to the cursor for the table we are trying
    # to interact with.

    # Most functions will interact with these 5 tables.
    if x == 0:
        print("1) Card")
        print("2) Character")
        print("3) Enemy")
        print("4) Potion")
        print("5) Relic")
        print()
        return input("Enter a table name or press any key to continue. \n> ").lower()

    # Current design for the win_rate function won't work for the Character
    # and Enemy tables as they have 0 and 2 connecting tables respectively,
    # compared to the 3 tables here that each only have the one connecting table.
    else:
        print("1) Card")
        print("2) Potion")
        print("3) Relic")
        print()
        return input("Enter a table name or press any key to continue. \n> ").lower()

def display_table(cursor, table_choice):
    # This function is reused often to show table information.
    # It will take table_choice from the requesting function
    # and display that table in a manner formatted for that
    # specific table

    if table_choice == "card":
        # For some reason, ORDER BY card_id does not work here
        cursor.execute(f"SELECT card_id, card_name FROM {table_choice}")
        
        print("ID    Name")
        for record in cursor.fetchall():
            # Name entries tables include a new line character that
            # need to be removed to display cleanly.
            name = str(record[1].replace("\n", ''))
            print("{:<5} {:<5}".format(record[0], name))

    # These tables only have ID and name as relevant items to display
    elif (table_choice == "character" 
            or table_choice == "encounter" 
            or table_choice == "enemy" 
            or table_choice == "potion"
            or table_choice == "relic"):
        cursor.execute(f"SELECT * FROM {table_choice}")
        print("ID    Name")
        for record in cursor.fetchall():
            name = record[1].replace("\n", '')
            print("{:<5} {:<5}".format(record[0], name))

    elif table_choice == "run":
        cursor.execute(f"SELECT * FROM {table_choice}")
        for record in cursor.fetchall():
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format("Run ID","Character ID","Ascension","Floor","W/L",))
            print("{:<10} {:<15} {:<15} {:<15} {:<15}".format(record[0],record[1],record[2],record[3],record[4],))
    
    elif table_choice == "encounter_has_enemy":
        cursor.execute(f"SELECT * FROM {table_choice}")
        print("ID    Enemy ID")
        for record in cursor.fetchall():
            print("{:<5} {:<5}".format(record[0], record[1]))

    elif (table_choice == "run_has_card"
            or table_choice == "run_has_encounter"
            or table_choice == "run_has_encounter"
            or table_choice == "run_has_potion"
            or table_choice == "run_has_relic"):
        cursor.execute(f"SELECT * FROM {table_choice}")
        print("ID1   ID2")
        for record in cursor.fetchall():
            print("{:<5} {:<5}".format(record[0], record[1]))

    else:
        pass
    print()
    
def add_item(cursor, connection):
    # Items can be added to the database
    # Primary key auto-incrementation and enforcement is not
    # currently working, requiring the item ID to be entered
    # manually by the user.

    table_choice = get_table_choice(0)
    
    if table_choice == "card":
        try:
            display_table(cursor, "character")
            char_id = input("Enter character ID > ")
            display_table(cursor, table_choice)
            card_id = input("Enter a unique card ID > ")
            name = input("\nEnter card name > ")
            card_keyword = input("\nEnter card keyword > ")
            card_type = input("\nEnter card type (Attack, Skill, or Power) > ")
            values = (card_id, char_id,name,card_keyword,card_type)
            cursor.execute("INSERT INTO card(card_id,character_id,card_name,keyword,type) VALUES(?,?,?,?,?)", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    # Following choices could potentially be combined
    # by changing Enter ___ name to Enter Item name        
    elif table_choice == "character":
        try:
            display_table(cursor, table_choice)
            id = input("Enter a unique ID > ")
            name = input("Enter character name > ")
            values = (id, name)
            cursor.execute(f"INSERT INTO {table_choice} ({table_choice}_id,{table_choice}_name) VALUES (?,?)", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "enemy":
        try:
            display_table(cursor, table_choice)
            id = input("Enter a unique ID > ")
            name = input("Enter an enemy name > ")
            values = (id, name)
            cursor.execute(f"INSERT INTO {table_choice} ({table_choice}_id,{table_choice}_name) VALUES (?,?)", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "potion":
        try:
            display_table(cursor, table_choice)
            id = input("Enter a unique ID > ")
            name = input("Enter potion name > ")
            values = (id, name)
            cursor.execute(f"INSERT INTO {table_choice} ({table_choice}_id,{table_choice}_name) VALUES (?,?)", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "relic":
        try:
            display_table(cursor, table_choice)
            id = input("Enter a unique ID > ")
            name = input("Enter relic name > ")
            values = (id, name)
            cursor.execute(f"INSERT INTO {table_choice} ({table_choice}_id,{table_choice}_name) VALUES (?,?)", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    else:
        pass

def update_item(cursor, connection):
    # Items can be updated in the database
    # Currently only designed to update the name
    # of an item. Further improvements can
    # be added to change other item variables.

    table_choice = get_table_choice(0)

    if table_choice == "card":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being updated > ")
            name = input("Enter new item name > ")
            values = (name, id)
            cursor.execute(f"UPDATE {table_choice} SET {table_choice}_name = ? WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    # Following tables should be joined.        
    elif table_choice == "character":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being updated > ")
            name = input("Enter new item name > ")
            values = (name, id)
            cursor.execute(f"UPDATE {table_choice} SET {table_choice}_name = ? WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "enemy":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being updated > ")
            name = input("Enter new item name > ")
            values = (name, id)
            cursor.execute(f"UPDATE {table_choice} SET {table_choice}_name = ? WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "potion":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being updated > ")
            name = input("Enter new item name > ")
            values = (name, id)
            cursor.execute(f"UPDATE {table_choice} SET {table_choice}_name = ? WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "relic":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being updated > ")
            name = input("Enter new item name > ")
            values = (name, id)
            cursor.execute(f"UPDATE {table_choice} SET {table_choice}_name = ? WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    else:
        pass

def delete_item(cursor, connection):
    # Items can be removed from the database
    # Items are referenced and removed by their
    # ID. The different tables can be consolidated
    # in this function.

    table_choice = get_table_choice(0)
    
    if table_choice == "card":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being removed > ")
            values = (id,)
            cursor.execute("DELETE FROM card WHERE card_id != ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")
            
    elif table_choice == "character":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being removed > ")
            values = (id,)
            cursor.execute(f"DELETE FROM {table_choice} WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")
    elif table_choice == "enemy":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being removed > ")
            values = (id,)
            cursor.execute(f"DELETE FROM {table_choice} WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "potion":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being removed > ")
            values = (id,)
            cursor.execute(f"DELETE FROM {table_choice} WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    elif table_choice == "relic":
        try:
            display_table(cursor, table_choice)
            id = input("Enter ID of item being removed > ")
            values = (id,)
            cursor.execute(f"DELETE FROM {table_choice} WHERE {table_choice}_id = ?", values)
            connection.commit()
            display_table(cursor,table_choice)
        except ValueError:
            print("There was an error. Try Again.")

    else:
        pass

def calculate_wr(cursor):
    # This function uses a SELECT statement with multiple joins and
    # subqueries to calculate the Win Rates for certain items.
    # The statement is currently broken, only working to pull informatation
    # for relics and not properly calculating the Win Rate


    table_choice = get_table_choice(1)
    test = True
    while test:
        if table_choice == 'card' or table_choice == 'relic' or table_choice == 'potion':
            test = False
            continue
        else:
            print("Invalid input, please select a new table.")
            table_choice = get_table_choice(1)
    display_table(cursor, table_choice)
    id = input("Enter ID of item > ")
    try:
        cursor.execute(f"WITH win_rate AS (SELECT rhr3.{table_choice}_id, ((SELECT count(rhr1.{table_choice}_id) FROM run_has_{table_choice} rhr1 JOIN run r ON rhr1.run_id = r.run_id WHERE r.win = 1 AND rhr1.{table_choice}_id = rhr3.{table_choice}_id) / (SELECT count(rhr2.{table_choice}_id) FROM run_has_{table_choice} rhr2 JOIN run r ON rhr2.run_id = r.run_id WHERE rhr2.{table_choice}_id = rhr3.{table_choice}_id)) AS win_rate, (SELECT count(rhr2.{table_choice}_id) FROM run_has_{table_choice} rhr2 JOIN run r ON rhr2.run_id = r.run_id WHERE rhr2.{table_choice}_id = rhr3.{table_choice}_id) AS number_of_runs FROM run_has_{table_choice} rhr3) SELECT re.{table_choice}_name,  wr.win_rate, wr.number_of_runs FROM {table_choice} re JOIN win_rate wr ON wr.{table_choice}_id = re.{table_choice}_id WHERE wr.win_rate IS NOT null AND re.{table_choice}_id LIKE '{id}' GROUP BY {table_choice}_name ORDER BY wr.win_rate DESC, wr.number_of_runs DESC, re.{table_choice}_name")
    except ValueError:
        print("There was an error. Try Again.")
    
    print("Item Name     Win Rate     # of Runs Used")
    for record in cursor.fetchall():
        name = record[0].replace("\n", '')
        print("{:<5} {:<5} {:<5}".format(name, record[1], record[2]))

def make_choice(cursor, connection):
    # This function is the first point of interaction in the program.
    # It will give the options for processes to be done in the database.
    # Until the user tells the program to quit, it will continue to ask for input.
    # Once a choice is made the associated function is called.

    choice = None
    while choice != "6":
        print("1) Display Table")
        print("2) Add Item")
        print("3) Update Item")
        print("4) Delete Item")
        print("5) Calculate Win Rate of Item")
        print("6) Quit")
        print()
        choice = input("Enter the number of the desired action > ")
        print()
        if choice == "1":
            # We do not use the get_table_choice function here so we can show other tables
            # that are not usuable with the other processes in the program (i.e. any run_has_* table)
            cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")
            print("Table Name:")
            for record in cursor.fetchall():
                name = record[0].capitalize()
                print(name)
                print()
            table_choice = input("Enter a table name for more contents, or press any key to continue. \n> ").lower()
            display_table(cursor, table_choice)
            
            
        elif choice == "2":
            add_item(cursor, connection)

        elif choice == "3":
            update_item(cursor, connection)

        elif choice == "4":
            delete_item(cursor, connection)

        elif choice == "5":
            calculate_wr(cursor)

        elif choice == "6":
            pass

        else:
            print("Sorry, I didn't catch that. What were you wanting?\n")



def main():
    # Main Function
    # Create connection to db and cursor object to interact

    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()
    
    make_choice(cursor, connection)

    pass    

if __name__ == "__main__":
    main()