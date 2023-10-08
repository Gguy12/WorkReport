import sqlite3
import pickle

def str2(s):
    if s is None:
        return 'NULL'
    if type(s) is str:
        return "'" + s + "'"
    return str(s)


class pilot(object):
    def __init__(self,User_Name,Password,Biometrics = "null"):
        self.User_Name = User_Name
        self.Password = Password
        self.Biometrics = Biometrics
        
    def add_Biometrics(self, Biometrics):
        """not a done function will add biometrics to the table"""
        db = User_Orm()
        db.open_DB()
        if self.Biometrics is None:
            #self.flight1 = Flight.id
            #sql = "UPDATE pilot SET first_flight_id = " + str2(Flight.id) + " WHERE id = " + str2(self.id)
            #res = db.current.execute(sql)
            db.commit()
            db.close_DB()
        else:
            return False

    def __str__(self):
        return str2(self.User_Name) + "," + str2(self.Password) + "," + str2(self.Biometrics)


class flight(object):
    def __init__(self, id, pilot1, pilot2, from_, to_, departure_time, duration, status="on time"):
        self.id = id
        self.pilot1 = pilot1
        self.pilot2 = pilot2
        self.from_ = from_
        self.to_ = to_
        self.departure_time = departure_time
        self.duration = duration
        self.status = status

    def __str__(self):
        return str2(self.id) + "," + str2(self.pilot1) + "," + str2(self.pilot2) + "," + str2(self.from_) + "," + \
               str2(self.to_) + "," + str2(self.departure_time) + "," + str2(self.duration) + "," + str2(self.status)


class User_Orm():
    def __init__(self):
        self.conn = None  # will store the DB connection
        self.cursor = None  # will store the DB connection cursor

    def open_DB(self):
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('database.db')
        self.current = self.conn.cursor()

    def close_DB(self):
        self.conn.close()

    def commit(self):
        self.conn.commit()

    # All read SQL
    def get_user(self, id):
        self.open_DB()

        sql = "select * from Users where User_Name = " + str(id)
        res = self.current.execute(sql)
        ans = res.fetchone()
        if ans == None:
            return False
        ans = 

        self.close_DB()
        return ans

    def get_all_users(self):
        self.open_DB()

        sql = "select * from Users"
        res = self.current.execute(sql)
        ans = res.fetchall()
        ans2 = []
        for Pilot in ans:
            ans2.append(User(ans[0],ans[1],ans[2]))

        self.close_DB()
        return ans2

    def add_user(self, User):
        self.open_DB()

        sql = "insert into Users (User_Name,Password,Biometrics) values(" + str(User) + ")"
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def remove_user(self, User_Name):
        self.open_DB()

        sql = "DELETE FROM Users where User_Name = " + str(User_Name)
        res = self.current.execute(sql)
        self.commit()

        self.close_DB()

    def get_flight(self, id):
        self.open_DB()

        sql = "select * from flight where id = " + str(id)
        res = self.current.execute(sql)
        ans = res.fetchone()
        ans = flight(ans[0], ans[1], ans[2], ans[3], ans[4], ans[5], ans[6], ans[7])

        self.close_DB()
        return ans

    def get_all_flights(self):
        self.open_DB()

        sql = "select * from flight"
        res = self.current.execute(sql)
        ans = res.fetchall()
        ans2 = []
        for Flight in ans:
            ans2.append(flight(Flight[0], Flight[1], Flight[2], Flight[3], Flight[4], Flight[5], Flight[6], Flight[7]))

        self.close_DB()
        return ans2

    def add_flight(self, Flight):
        self.open_DB()

        sql = "insert into flight (id,first_pilot_id,second_pilot_id,from_,to_,departure_time,duration,status) " \
              "values(" + str(Flight) + ") "
        print(sql)
        res = self.current.execute(sql)

        self.commit()
        self.close_DB()

    def remove_flight(self, id):
        self.open_DB()

        sql = "DELETE FROM flight where id = " + str(id)
        res = self.current.execute(sql)
        self.commit()

        self.close_DB()

    def fill_flight(self, Flight, pilot1, pilot2=None):

        if Flight.pilot2 is not None:
            return False

        if pilot2 is not None and Flight.pilot1 is not None:
            return False
        self.open_DB()
        if Flight.pilot1 is not None and pilot2 is None:
            Flight.pilot2 = pilot1.id
            pilot1.add_flight(Flight)

            sql = "UPDATE flight SET second_pilot_id = " + str2(Flight.pilot2) + " WHERE id = " + str2(Flight.id)
            res = self.current.execute(sql)
            self.commit()

        else:
            Flight.pilot1 = pilot1.id
            pilot1.add_flight(Flight)
            Flight.pilot2 = pilot2.id
            pilot2.add_flight(Flight)

            sql = "UPDATE flight SET first_pilot_id = " + str2(Flight.pilot1) + " WHERE id = " + str2(Flight.id)
            res = self.current.execute(sql)
            self.commit()

            sql = "UPDATE flight SET second_pilot_id = " + str2(Flight.pilot2) + " WHERE id = " + str2(Flight.id)
            res = self.current.execute(sql)
            self.commit()

        self.close_DB()

    def cancel_flight_without_pilots(self):
        self.open_DB()

        sql = "update flight set status = 'canceled' where second_pilot_id is NULL"
        res = self.current.execute(sql)
        self.commit()

        self.close_DB()