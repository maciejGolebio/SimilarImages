import sqlite3


class DBConector:
    @staticmethod
    def createDataBase():
        conn = sqlite3.connect('projekt_zesp.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IMAGE
                     (Id INTEGER PRIMARY KEY NOT NULL ,path text NOT NULL, name text NOT NULL)''')
        c.execute('''CREATE TABLE VIRTUALFOLDER
                     (Id INTEGER PRIMARY KEY NOT NULL , name text NOT NULL)''')
        c.execute('''CREATE TABLE VIRTUALFOLDER_IMAGE
                     (IMAGE_Id REFERENCES IMAGE(Id),VIRTUALFOLDER_Id REFERENCES VIRTUALFOLDER(Id))''')

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        conn.close()


#
#DBConector.createDataBase()
