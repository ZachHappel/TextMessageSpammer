import random
import sys
import os
import re
import fileinput
from datetime import datetime
import time
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText
from flask import Flask, flash, redirect, render_template, json, request, session, abort
# from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

numberoftimes = ''
sender = ''
destination = ''
USERNAME = "@textmessagespammer.com"
PASSWORD = ""
text_subtype = 'plain'
subject = ""
listoftimes = ['0', '25', '50', '75', '100', '200', '300', '400', '500']
stime_to_wait = ''

print("starting")

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = 'donttellanewon'

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'webserve_01'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'webserve_forms'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

mysqlconn = mysql.connect()
cursor = mysqlconn.cursor()

isnumbergood = False






def emailcycler():
    print("emailcycler")
    global xxxint
    global finalxxx
    global sender
    global stringxxx
    xxxint = random.randint(1, 25)  # creates int 1-25
    stringxxx = str(xxxint)  # takes int and converts to string, in order to use len it has to be a string
    if len(stringxxx) == 1:  # if len of string is 1 (e.g #6)
        finalxxx = "00" + stringxxx  # 6 --> 006
    elif len(stringxxx) == 2:  # if len of string is 2 (e.g #16)
        finalxxx = "0" + stringxxx  # 16 --> 016
    sender = finalxxx + '@textmessagespammer.com'  # 016@webservertest3737.info
    print("this is sender:" + str(sender))


@app.route('/')
def redir():
    return redirect("/index.html", code=302)


@app.route("/timetowait/<string:stime_to_wait>/")
def failpage(stime_to_wait):
    return render_template('returnpage.html', stime_to_wait = stime_to_wait)

@app.route('/index.html', methods=['POST'])
def sendmess_post():
    value = request.form['number']
    global isnumbergood
    vlen = len(value)
    now = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open("/home/webserve/FlaskSMS/FlaskSMS/dict.rtf", "r+") as f:
        searchfile = f.readlines()
        f.close()

    with open('/home/webserve/FlaskSMS/FlaskSMS/dict.rtf', 'r') as d:
        filedata = d.read()
        d.close

    for i, line in enumerate(searchfile):
        print(i)
        if value == '8455534651': 
            quit()
        else:
            pass
        if value in line:
            value_in_line = True
            day = str(line[vlen + 10:-10])
            # print("This is day:"+day+".")
            # nowday = str(now[8:-9])
            # print("THis is now day:"+nowday+".")
            # print("this is line:"+line)
            # day_plus = int(day) + 1
            # print("  ----- -")
            # print(int(now[8:-9]))
            # print("this is day + 1:" + str(day_plus))
            if str(now[8:-9]) == day:
                # print("Hello?")
                indata_hour = int(line[vlen + 13:-7])
                hour_difference = abs(indata_hour - int(now[11:-6]))
                if hour_difference >= 12:
                    # print("You can send your message.")
                    # print("this is line: " + line)
                    # print("this is now: " + now)
                    filedata = filedata.replace(line, (value + ": " + now + "\n"))
                    with open('/home/webserve/FlaskSMS/FlaskSMS/dict.rtf', 'w') as d:
                        d.write(filedata)
                        d.close()
                        isnumbergood = True
                        print("You can send")

                        #      FLASH ! ! ! !
                else:
                    time_to_wait = 12 - hour_difference
                    # messags = 'Please try again in %s hours!' % time_to_wait
                    stime_to_wait = str(time_to_wait)
                    print('Please try again in %s hours!' % stime_to_wait)
                    isnumbergood = False
                    #      FLASH ! ! ! !

            elif int(now[8:-9]) == int(day) + 1:
                print((int(now[11:-6])))
                print((24 - int(line[vlen + 13:-7])))
                difference_between_days = ((int(now[11:-6])) + (24 - int(line[vlen + 13:-7])))
                # difference_between_days = abs(int(now[11:-6]) - (24-int(line[vlen+13:-7])))
                print(difference_between_days)
                if difference_between_days >= 12:
                    filedata = filedata.replace(line, (value + ": " + now + "\n"))
                    with open('/home/webserve/FlaskSMS/FlaskSMS/dict.rtf', 'w') as d:
                        d.write(filedata)
                        d.close()
                        print("You can send!")
                        isnumbergood = True
                        #      FLASH ! ! ! !
                else:
                    time_to_wait = 12 - difference_between_days
                    isnumbergood = False
                    stime_to_wait = str(time_to_wait)
                    print("Please try again in %s hours!" % stime_to_wait)
 


                    #      FLASH ! ! ! !

            elif int(now[8:-9]) > int(day) + 1:
                filedata = filedata.replace(line, (value + ": " + now + "\n"))
                with open('/home/webserve/FlaskSMS/FlaskSMS/dict.rtf', 'w') as d:
                    d.write(filedata)
                    d.close()
                    print("You're all good to send. ")
                    isnumbergood = True
            else:
                pass





        else:
            value_in_line = False

    if value_in_line == False:
        isnumbergood = True
        with open('/home/webserve/FlaskSMS/FlaskSMS/dict.rtf', 'a') as t:
            t.write((value + ": " + now + "\n"))
            t.close()
    else:
        pass
        
    if isnumbergood == True:
        timesent = 0
        global destination
        print("sending?")
        global numberoftimes
        carrier = str(request.form['provider'])

        # "%s" % request.form['options']
        createreciever = str(request.form['number']) + carrier

        destination = [createreciever]
        times = int(request.form['howmany'])
        numberoftimes = int(listoftimes[times])
        text = request.form['number']
        text = request.form['message']
        text = request.form['howmany']
        processed_text = text.upper()
        print("this is destination: " + str(destination))
        print("this is number: " + str(request.form['number']))
        print("this is how message: " + str(request.form['message']))
        print("this is how many: " + str(request.form['howmany']))
        content = """\
        %s
        """ % str(request.form['message'])
        try:
            _number = request.form['number']
            _message = request.form['message']
            _howmany = request.form['howmany']
            _carrier = request.form['provider']
            _checknumber = request.form['number']

            # validate the received values
            if _number and _message and _howmany and _carrier:

                # All Good, let's call MySQL

                sqlconn = mysql.connect()
                cursor = sqlconn.cursor()
                # _hashed_password = generate_password_hash(_password)
                cursor.callproc('sp_AllDatasend', (_number, _message, _howmany, _carrier, _checknumber))
                data = cursor.fetchall()

                if len(data) is 0:
                    sqlconn.commit()
                    # return json.dumps({'message':'User created successfully !'})
                else:
                    pass
                    # return json.dumps({'error':str(data[0])})
            else:
                pass
                # return json.dumps({'html':'<span>Enter the required fields</span>'})

        except Exception as e:
            return json.dumps({'error': str(e)})
        finally:
            cursor.close()
            sqlconn.close()

        while timesent <= int(numberoftimes):
            try:
                print("trying to send")
                emailcycler()
                msg = MIMEText(content, text_subtype)
                msg['Subject'] = subject
                msg['From'] = sender  # some SMTP servers will do this automatically, not all
                print("balls")
                SMTPserver = 'mail.textmessagespammer.com'
                conn = SMTP(SMTPserver)
                print("a")
                conn.set_debuglevel(False)
                print("b")
                conn.login(sender, PASSWORD)
                print("hello")
                try:
                    conn.sendmail(sender, destination, msg.as_string())
                    conn.quit()
                    timesent += 1
                    if timesent == int(numberoftimes):
                        return render_template('successpage.html')
                    elif timesent == 2:
                    	pass
                    	#return render_template('successpage.html')

                except:
                    print("Something went wrong.")
            except:
                print("Something went wrong.")
        if timesent > int(numberoftimes):
            quit()
    else:
        return redirect("/timetowait/%s/"%stime_to_wait)
        time.sleep(20)
        quit()
#

@app.route("/index.html")
def index():
    return render_template('layout.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            sqlconn = mysql.connect()
            cursor = sqlconn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser', (_name, _email, _hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                sqlconn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        sqlconn.close()


@app.route("/hello/<string:name>/")
def hello(name):
    return render_template('test.php', name=name)



@app.route('/Info')
def info():
    return render_template('infonew.html')


@app.route('/ourPlans')
def ourplans():
    return render_template('plans.html')



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)

print("uh ok")





