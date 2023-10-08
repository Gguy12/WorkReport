import sqlite3

import pickle
    # https://docs.python.org/2/library/sqlite3.html
    # https://www.youtube.com/watch?v=U7nfe4adDw8


__author__ = 'Gooch'


class Car():
    def __init__(self, model, whight, speed, wheel_size, color, hight, seat_num, price, tank_capacity, company):
        self.model = model
        self.whight = whight
        self.speed = speed
        self.wheel_size = wheel_size
        self.color = color
        self.hight = hight
        self.seat_num = seat_num
        self.tank_capacity = tank_capacity
        self.price = price
        self.company = company
        

    def new_color(self,new_color):
        self.color= new_color


    def change_seat_num(self, new_seat_num):
        self.change_seat_num= new_seat_num


    def __str__(self):
        return "car:", self.whight, ":", self.speed,":", self.wheel_size, ":", self.color, ":", self.hight, ":", self.seat_num, ":", self.tank_capacity, ":", self.price, ":", self.model, ":", self.company


class CarCompany(object):
    def __init__(self, name, models_num, ceo,):
        self.name = name
        self.models_num = models_num
        self.ceo = ceo
        




    
class CarCompanyORM():
    def __init__(self):
        self.conn = sqlite3.connect('carscompanys.db')  # will store the DB connection
        self.cursor = self.conn.cursor()   # will store the DB connection cursor

    
    def create_table(self, table_name, *args): #
        self.open_DB()

        command1 = """CREATE TABLE IF NOT EXISTS """ + table_name + """(""" 
        for arg in args:
            command1 += arg + "," 
        command1 = command1[:-1] + """)"""

        print(command1)
        self.cursor.execute(command1)

        self.conn.commit()
        self.close_DB


    def open_DB(self): #
        """
        will open DB file and put value in:
        self.conn (need DB file name)
        and self.cursor
        """
        self.conn = sqlite3.connect('carscompanys.db')
        self.cursor=self.conn.cursor()
        
        
    def close_DB(self): #
        self.conn.close()

    def fetch_all(self):
        print(self.cursor.fetchall())


    #All read SQL

    def get_car_by_model(self,model):#
        self.open_DB()

        sql = "SELECT * FROM cars WHERE model=" + '"' + model + '";'
        print("get car by model: " + sql)
        res= self.cursor.execute(sql)
        car = self.cursor.fetchone()

        self.close_DB()
        return car
    
    def GetCompanies(self): #
        self.open_DB()

        sql = """SELECT * FROM "companies" """
        res = self.cursor.execute(sql)
        companies = self.cursor.fetchall()

        self.close_DB()
        return companies
        


    def GetCars(self):#
        self.open_DB()
        
        sql = "SELECT * FROM cars"
        self.cursor.execute(sql)
        cars = self.cursor.fetchall()

        self.close_DB()
        return cars


    def get_car_ceo(self,model):# 
        self.open_DB()

        sql="SELECT a.ceo FROM companies a , cars b WHERE a.name=b.company"
        res = self.cursor.execute(sql)
        ceo = self.cursor.fetchone()

        self.close_DB()
        return ceo


    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #______end of read start write ____________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________
    #__________________________________________________________________________________________________________________




    #All write SQL

#  model, whight, speed, wheel_size, color, hight, seat_num, price, tank_capacity, company
    def insert_car(self, car: Car):#
        self.open_DB()
        
        sql = 'INSERT INTO cars VALUES ("' + car.model + '", "' + car.whight+ '", "' + car.speed+ '", "' + car.wheel_size+ '", "' +car.color+ '", "' +car.hight+ '", "' +car.seat_num+ '", "' +car.price+ '", "' +car.tank_capacity+ '", "' +car.company + '")'
        print("insert car: "+ sql)
        self.cursor.execute(sql)

        self.conn.commit()
        self.close_DB()
        return 


    def insert_company(self, company: CarCompany): #
        self.open_DB()

        sql = 'INSERT INTO companies VALUES ("' + company.name + '", "'  +company.models_num+ '", "' +company.ceo + '")'
        print("insert_company: ", sql)
        self.cursor.execute(sql)
        
        self.conn.commit()

        self.close_DB()
        


    def delete_company_by_name(self, name): #
        self.open_DB()
        
        sql = "DELETE FROM companies WHERE name=" + '"' + name + '"'
        print("delete company: " + sql)
        self.cursor.execute(sql)

        self.conn.commit()
        self.close_DB()
        return 
        

    def delete_car_by_model(self, model):#
        self.open_DB()

        sql = "DELETE FROM cars WHERE model=" + '"' + model + '"'
        print("delete company: " + sql)
        self.cursor.execute(sql)

        self.conn.commit()
        self.close_DB()
        return 
