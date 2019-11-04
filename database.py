import sqlite3 as sql
import pickle
class all_students:

    def check(adno):
        try:
            fr=open("std_adno.pickle","rb")
            std = pickle.load(fr)
            fr.close()
            if adno not in std:
                std.append(adno)
                fw=open("std_adno.pickle","wb")
                pickle.dump(std,fw)
                fw.close()
                return(True)
            elif adno in std:
                return(False)

        except:
            std=[adno]
            fw=open("std_adno.pickle","wb")
            pickle.dump(std,fw)
            fw.close()
            return(True)
            
    def add_data(name,email,ph,clas,adno):
        try:
            db=sql.connect('students.db')
            cnn=db.cursor()
            cmd='CREATE TABLE IF NOT EXISTS Clients(Name TEXT,Email TEXT UNIQUE,Phone TEXT,Class TEXT,Ad_No TEXT UNIQUE)'
            cnn.execute(cmd)
            cnn.execute('INSERT INTO Clients(Name,Email,Phone,Class,Ad_No)VALUES (?,?,?,?,?)',(name,email,ph,clas,adno))
            db.commit()
            return(True)
        except:
            return(False)

    def lcheck(adno):
        
        fr=open("std_adno.pickle","rb")
        std = pickle.load(fr)
        fr.close()
        if adno  in std:
            return(True)
        else:
            return(False)

    def get_info(adno):

        db=sql.connect('students.db')
        cnn=db.cursor()
        info=cnn.execute('SELECT Name,Email,Ad_No FROM Clients WHERE Ad_No IS ?',(adno,))
        info=info.fetchall()[0]
        return info
#a=all_students
#b=a.get_info("2018bcs1011")
#print(b)
#c=a.add_data("Vidit","Email4","phone","CSE-2","2018bcs1174")
#print(c)





                              
