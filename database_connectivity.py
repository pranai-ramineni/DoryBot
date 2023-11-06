import mysql.connector

def DataUpdate(FirstName,Feedback,logFileName):
    mydb = mysql.connector.connect(host='127.0.0.1', user="root", password="root", auth_plugin='mysql_native_password', database="rasa_feedback")

    with open(logFileName) as f:
        chatLogs = f.read()
        print(chatLogs)

    mycursor = mydb.cursor()
    sql ='INSERT INTO rasa_feedback_logs_new1 (firstName, feedback, chatLogs) VALUES ("{0}", "{1}", "{2}");'.format(FirstName,Feedback,chatLogs)
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

#if __name__ == '__main__':
    #DataUpdate("Sakshi","good Session")