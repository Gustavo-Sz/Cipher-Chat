import sqlite3
import os


class databaseClass:

    def __init__(self):
        self.__locale = f"{os.getcwd()}\\db.db"
        self.__connectdb = sqlite3.connect(self.__locale)

    def closedb(self):
        self.__connectdb.close()

    def get(self, table, colunas, where):

        aux = ""
        for x in range(len(colunas)):
            if x < len(colunas)-1:
                aux += f"{colunas[x]}, "
            else:
                aux += colunas[x]
        sql = f"SELECT {aux} FROM {table}"
        if len(where) != 0:
            for x in range(int(len(where)/2)):
                if x == 0:
                    sql += f" WHERE {where[x]} = '{where[x+1]}'"
                else:
                    sql += f" AND {where[x*2]} = '{where[(x*2)+1]}'"
        cur = self.__connectdb.cursor()
        cur.execute(sql)
        return cur.fetchall()

    def insert(self, table, values):

        aux = ""
        valueslist = []
        for x in range(len(values)):
            if x < len(values)-1:
                aux += "?, "
                valueslist.append(values[x])
            else:
                aux += "?"
                valueslist.append(values[x])

        sql = f"INSERT into {table} VALUES ({aux})"
        cur = self.__connectdb.cursor()
        cur.execute(sql, valueslist)
        self.__connectdb.commit()

    def update(self, table, set, where):

        sql = f"UPDATE {table} SET {set[0]} = {set[1]} WHERE {where[0]} = {where[1]}"
        cur = self.__connectdb.cursor()
        cur.execute(sql)
        self.__connectdb.commit()

    def delete(self, table, where):

        sql = f"DELETE FROM {table} WHERE {where[0]} = {where[1]}"
        cur = self.__connectdb.cursor()
        cur.execute(sql)
        self.__connectdb.commit()
