import pymysql

class database:
    def __init__(self):
        self.db = pymysql.connect(host= '127.0.0.1', port= 3306, user= 'root', password= 'abc839986',db='demo')
        self.cursor = self.db.cursor()

    def insert_single(self , address , port , lastTime ,type):

        into = "INSERT INTO lagou(address,port,lastTime , type) VALUES (%s, %s, %s ,%s)"
        values = (address, port, lastTime , type)

        try:
            self.cursor.execute(into , values)
            self.db.commit()

        except Exception as e:
            print(e)
            self.db.rollback()

    def insert_multiple(self,values):
        req = []
        for i in range(len(values)):
            address = values[i]['address']
            port = values[i]['port']
            lastTime = values[i]['lastTime']
            type = values[i]['type']
            req.append((address , port , lastTime , type))

        sql = "INSERT INTO ip(address,port,lastTime,type) VALUES (%s, %s, %s,%s)"
        self.cursor.executemany(sql , req)
        self.db.commit()

    def removeAll(self):
        sql = "TRUNCATE TABLE ip"
        self.cursor.execute(sql)
        pass

    def remove(self):
        pass

    def modify(self):
        pass

    def search(self):
        sql = "SELECT * FROM ip"
        self.cursor.execute(sql)
        IParr = []
        results = self.cursor.fetchall()
        for item in results:
            address = item[1]
            port = item[2]
            type = item[4]
            IParr.append(str.lower(type) + '://' + address + ':' + str(port))

        return IParr



    def close(self):
        self.db.close()

# if __name__ == '__main__':
#     obj = database()
#     obj.insert_single()
#     obj.quit()