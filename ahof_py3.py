import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print("Error:create_database: " + str(e))
    return connection

def create_table(connection, sql_create_table):
    try:
        cursor = connection.cursor()
        cursor.execute(sql_create_table)
        connection.commit()
    except Error as e:
        print("Error: create_table: " + str(e))

def insert_into_table(connection, table, title, author, genre, themes, medium):
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO " + table + " VALUES (?, ?, ?, ?, ?)", (title, author, genre, themes, medium))
        connection.commit()
    except Error as e:
        print("Error: insert_into_table: " + str(e))

def search_in_table(connection, table, title, author, genre, theme, medium):
    try:
        cursor = connection.cursor()
        query = ""
        if title != "":
            query += " title LIKE '%" + title + "%'"
        if author != "":
            if query != "":
                query += " AND author LIKE '%" + author + "%'"
            else:
                query += " author LIKE '%" + author + "%'"
        if genre != "":
            if query != "":
                query += " AND genre LIKE '%" + genre + "%'"
            else:
                query += " genre LIKE '%" + genre + "%'"
        if theme != "":
            if query != "":
                query += " AND themes LIKE '%" + theme + "%'"
            else:
                query += " themes LIKE '%" + theme + "%'"
        if medium != "":
            if query != "":
                query += " AND medium LIKE '%" + medium + "%'"
            else:
                query += " medium LIKE '%" + medium + "%'"
        full_query = "SELECT * FROM " + table + " WHERE" + query
        print(full_query)
        cursor.execute(full_query)
        rows = cursor.fetchall()
        c = 0
        for row in rows:
            c = c + 1
            print("-------------------------------------------------------------------------------------------")
            print("Title: " + row[0])
            print("Author: " + row[1])
            print("Genre(s): " + row[2])
            print("Theme(s): " + row[3])
            print("Medium: " + row[4])
        print("-------------------------------------------------------------------------------------------")
        print("There are " + str(c) + " entries")
        cursor.close()
        connection.commit()
    except Error as e:
        print("Error: search_in_table: " + str(e))

def print_table(connection, table):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM " + table)
        connection.commit()
        rows = cursor.fetchall()
        amount = 0
        for row in rows:
            amount += 1
            print("-------------------------------------------------------------------------------------------")
            print("Title: " + row[0])
            print("Author: " + row[1])
            print("Genre(s): " + row[2])
            print("Theme(s): " + row[3])
            print("Medium: " + row[4])
        print("-------------------------------------------------------------------------------------------")
        print("There are " + str(amount) + " entries")
    except Error as e:
        print("Error: print_table: " + str(e))

def remove_from_table(connection, table, searchkey):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM " + table + " WHERE title=?", (searchkey,))
        connection.commit()
    except Error as e:
        print("Error: remove_from_table: " + str(e))

def add(connection, table):
    title = input("Title: ")
    author = input("Author: ")
    genre = input("Genre(s): ")
    themes = input("Themes: ")
    medium = input("Medium: ")
    insert_into_table(connection, table, title, author, genre, themes, medium)

def remove(connection, table):
    title = input("Title: ")
    remove_from_table(connection, table, title)

def search(connection, table):
    title = input("Title: ")
    author = input("Author: ")
    genre = input("Genre(s): ")
    theme = input("Theme(s): ")
    medium = input("Medium: ")
    search_in_table(connection, table, title, author, genre, theme, medium)

def clear(connection, table):
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM " + table)
        cursor.execute("VACUUM")
        connection.commit()
    except Error as e:
        print("Error: clear: " + str(e))

def main():
    database = r"/sqlite/db/ahof.db"
    connection = create_connection(database)
    sql_create_art_table = """CREATE TABLE IF NOT EXISTS art (
                                title text,
                                author text,
                                genre text,
                                themes text,
                                medium text
                                )"""
    create_table(connection, sql_create_art_table)
    option = 5
    
    while option != 0:
        print("Choose an option:\n0: quit\n1: add\n2: remove\n3: search\n4: display all\n5: clear")
        option = input()
        option = int(option)        
        if option == 0:
            break
        elif option == 1:
            add(connection, "art")
        elif option == 2:
            remove(connection, "art")
        elif option == 3:
            search(connection, "art")
        elif option == 4:
            print_table(connection, "art")
        elif option == 5:
            yesno = input("ARE YOU SURE (y/n): ")
            if yesno == "y" or yesno == "yes":
                clear(connection, "art")
            else:
                print("nothing cleared")
        else:
            print("Not an option")
main()

