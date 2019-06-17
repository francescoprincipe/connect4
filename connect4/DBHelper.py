import config as cfg
import sqlite3
import re #extract float from string

class DBHelper():
    #A class that manages the database

    def __init__(self, name_table, name_db = cfg.NAME_DB):
        self.name_db    = name_db
        self.name_table = name_table

    def __string_to_qs_list(self, str_qs):
        # Private method that convert a string qs to list qs
        qs = [float(s) for s in re.findall(r'-?\d+\.?\d*', str_qs)]
        return qs

    def select_all_row(self):
        # A function that execute a query select

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Execute a query
        sql = "SELECT * FROM {}".format(self.name_table)
        cursor.execute(sql)

        # Get results from the cursor
        rows = cursor.fetchall()

        # Close database connection
        connection.close()

        return rows

    def exists_state(self, state):
        # A function that return
        # - False ,if state not stored in db
        # - True ,if there's the state in db

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Prepare a list of arguments
        args = []
        args.append(str(state))

        ## Search a state in table Qs
        sql = "SELECT count(*) FROM {} WHERE state=?".format(self.name_table)
        cursor.execute(sql,args)

        # Get results from the cursor
        stored = cursor.fetchone()[0]

        # Close database connection
        connection.close()

        if stored == 0:
            return False
        else:
            return True

    def get_qs(self, state):
        # A function that return a qs tuple for a state

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Prepare a list of arguments
        args = []
        args.append(str(state))

        ## Search a state in table Qs
        sql = "SELECT q FROM {} WHERE state=?".format(self.name_table)
        cursor.execute(sql,args)

        # Get results from the cursor
        qs = cursor.fetchone()[0]

        # Close database connection
        connection.close()

        # Convert string to array
        return self.__string_to_qs_list(qs)

    def delete_all_row(self):
        # A function that delete all ros in table Qs

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Execute a query
        sql = "DELETE FROM {}".format(self.name_table)
        cursor.execute(sql)

        # Close database connection
        connection.close()

    def create_table(self):
        # A function that execute a query select

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Execute a query


        sql = "CREATE TABLE IF NOT EXISTS {} (state text primary key, q text not null)".format(self.name_table)
        cursor.execute(sql)

        # Close database connection
        connection.close()

    ## NOTE: Two strings as arguments
    def update_row(self, state, qs):
        # Update a row

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Prepare a list of arguments
        args = []
        args.append(qs)
        args.append(state)

        # Execute a query
        sql = "UPDATE {} set q = ? where state=?".format(self.name_table)
        cursor.execute(sql,args)

        updated = cursor.rowcount

        # Commit your changes in the database
        connection.commit()

        # disconnect from server
        connection.close()

        if updated == 0:
            return False
        else:
            return True

    ## NOTE: Two strings as arguments
    def insert_row(self, state, qs):
        # Insert a row

        # Open database connection
        connection = sqlite3.connect(self.name_db)

        # Prepare a cursor object using cursor() method
        cursor = connection.cursor()

        # Prepare a list of arguments
        args = []
        args.append(state)
        args.append(qs)

        # Execute a query
        sql = "INSERT INTO {}(state, q) VALUES (?,?)".format(self.name_table)
        cursor.execute(sql,args)

        # Commit your changes in the database
        connection.commit()

        # disconnect from server
        connection.close()
