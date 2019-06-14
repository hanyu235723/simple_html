
from bottle import request, jinja2_template,run,TEMPLATE_PATH,route,static_file
import sqlite3
import smtplib
from email.message import EmailMessage

TEMPLATE_PATH.append('./templates')
TEMPLATE_PATH.append('./static')
static_folder="./templates"
@route('/',method="get")
def main():
    return jinja2_template("main.html")

@route('/static/<filename>.css')
def server_static(filename):
#    print ("srs",static_file('{}.css'.format(filename),root="E:/My project/height collector/static"))
    return (static_file('{}.css'.format(filename),root="E:/My project/height collector/static"))

@route('/',method="post")
def check_height():
    email=request.forms["email_name"]
    height=request.forms["height_name"]
    total,avg_height= get_from_database(email, height)
    message = "The average height is {} out of {} persons".format(avg_height,total)
    sent_email(email,message)
    return jinja2_template('successful.html')

def  get_from_database(email,height):
    total_height=0
    conn=sqlite3.connect("height_record.db")
    c=conn.cursor()
    c.execute("create table if not exists height_record (id integer primary key autoincrement,email text,height integer)")
    c.execute("insert into height_record (email,height) values (?,?)",(email,height))
    conn.commit()
    rows =c.execute("select * from height_record").fetchall()
    total=len(rows)
    for row in rows:
        total_height+=row[2]
    average_height=total_height/total
    conn.close()
    return (total,average_height)

def get_all():
    conn = sqlite3.connect("height_record.db")
    c = conn.cursor()
    rows=c.execute("select * from height_record").fetchall()
    for row in rows:
        print (row)
    conn.close()

def sent_email(to_email,content):
    msg = EmailMessage()
    msg["Subject"]="The average height "
    msg["Frome"]="hanyuyu2018@gmail.com"
    msg["To"]:to_email
    msg.set_content(content)
# Send the message via our own SMTP server.
    s = smtplib.SMTP('host=localhost',port=25)
    s.send_message(msg)
    s.quit()

run(host='localhost', port=8000, debug=True, reloader=True)
