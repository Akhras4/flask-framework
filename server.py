from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)
app.secret_key = "#put any password"


@app.route('/')
def home():
    return render_template("indix.html", content=" welcome")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        password = request.form["password"]
        from sql import database

        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password for database",
            database="#databasename"
        )
        mycursor = mydb.cursor()
        n = "SELECT firstname FROM profile"
        p = "SELECT password FROM profile"
        mycursor.execute(n)
        myresult = mycursor.fetchall()
        for x in myresult:
            if x == (user,):
                mycursor.execute(p)
                myresult1 = mycursor.fetchall()
                for y in myresult1:
                    if y == (password,):
                        return redirect(url_for("user", usr=user))
        else:
            return render_template("login.html",
                                   contents="your password or email")
    else:
        return render_template("login.html")


@app.route("/<usr>")
def user(usr):
    return f' <h1> welcome {usr}</h1>'


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form["Firstname"]
        lastname = request.form["lastname"]
        email = request.form["email"]
        passworduser = request.form["password"]
        confirms = request.form["confirms"]
        berth = request.form["berth"]

        userandpass = {

        }
        n = 0
        m = 0
        o = 0
        p = 0
        alpha_array = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q',
                       'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'z',
                       'x', 'c', 'v', 'b', 'n', 'm']
        capital_array = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                         'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O',
                         'P', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        symbol_array = ["!", "@", "#", "$", "%", "^", "&", "*",
                        "(", ")", "-", "_", "=", "+", "{", "}",
                        ":", ";", "<", ">", "?", ".", "/", ",", "|"]
        number_array = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        if len(passworduser) <= 9:
            return render_template("signup.html", mserrorpassword="password error")

        else:
            for x in passworduser:  # check password
                for x4 in number_array:
                    if x4 == x:
                        p += 1
                for x3 in symbol_array:
                    if x3 == x:
                        o += 1
                for x2 in capital_array:
                    if x == x2:
                        m += 1
                for x1 in alpha_array:
                    if x == x1:
                        n += 1
            if n == 0 or m == 0 or p == 0:
                return render_template("signup.html", mserrorpassword="password error")

        if passworduser != confirms:
            return render_template("signup.html", msconfirmspassword='not equal')
        import mysql.connector
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#password for database",
            database="#databasename"
            
        )
        mycursor = mydb.cursor()
        n = "SELECT firstname FROM profile"
        m = "SELECT email FROM profile"
        mycursor.execute(n)
        myresult = mycursor.fetchall()
        for x in myresult:
            if x == (name,):
                return render_template("signup.html", msname="sorry The name is already exist")
            mycursor.execute(m)
            myresult1 = mycursor.fetchall()
            for y in myresult1:
                if y == (email,):
                    return render_template("signup.html", msemail="sorry tha email has already acess")

        else:
            import random
            number1 = random.randint(1001, 9999)

            import smtplib, ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            sender_email = '#put your email'
            receiver_email = email
            password = '#put your email passwod'

            message = MIMEMultipart("alternative")
            message["Subject"] = "multipart test"
            message["From"] = '#put your email'
            message["To"] = email

            # Create the plain-text and HTML version of your message
            text = f'{number1}' """\
            Hi,
            How are you?
            the number for login is    
            """
            f'{number1}'
            html = """\
            <html>
              <body>
                <p>Hi,<br>
                     How are you?<br>
                     <a href="http://www.realpython.com">number is </a> 
                      hallo.
                </p>
              </body>
            </html>
            """

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            # part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            # message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )
                session['name'] = name
                session['lastname'] = lastname
                session['email'] = email
                session['password'] = passworduser
                session['berth'] = berth
                session['number1'] = number1

            return redirect(url_for("numbermail"))

    else:
        return render_template("signup.html")


@app.route("/numbermail", methods=["POST", "GET"])
def numbermail():
    if request.method == "POST":
        name = session.get('name')
        lastname = session.get('lastname')
        email = session.get('email')
        password = session.get('password')
        berth = session.get('berth')
        number1 = session.get('number1')
        number = request.form["number"]
        if number == str(number1):
            import mysql.connector
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="# database password",
                database="#dtabase name"
            )
            mycursor = mydb.cursor()
            sql = "INSERT INTO profile (firstname, lastname, email, password, berth) VALUES (%s, %s, %s,%s,%s)"
            val = (name, lastname, email, password, berth)
            mycursor.execute(sql, val)
            mydb.commit()
            return redirect(url_for("user", usr=name))
        else:
            return render_template("numbermail.html", mserror="the number is not correct try again")

    else:
        return render_template("numbermail.html")


@app.route("/losspassword", methods=["POST", "GET"])
def losspassword():
    if request.method == "POST":
        email1 = request.form["email"]
        berth1 = request.form["berth"]
        import mysql.connector
        import random
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#password for database",
            database="#databasename""
        )
        mycursor = mydb.cursor()
        n = "SELECT email FROM profile"
        m = "SELECT berth FROM profile"
        mycursor.execute(n)
        myresult = mycursor.fetchall()
        for x in myresult:
            if x == (email1,):
                mycursor.execute(m)
                myresult1 = mycursor.fetchall()
                for y in myresult1:
                    if y == (berth1,):
                        import random
                        number2 = random.randint(1001, 9999)

                        import smtplib, ssl
                        from email.mime.text import MIMEText
                        from email.mime.multipart import MIMEMultipart

                        sender_email = '#your email'
                        receiver_email = email1
                        password = '#emailpassword'

                        message = MIMEMultipart("alternative")
                        message["Subject"] = "multipart test"
                        message["From"] = '#your email'
                        message["To"] = email1

                        # Create the plain-text and HTML version of your message
                        text = f'{number2}' """\
                              Hi,
                              How are you?
                              the number for login is    
                              """
                        f'{number2}'
                        html = """\
                              <html>
                                <body>
                                  <p>Hi,<br>
                                       How are you?<br>
                                       <a href="http://www.realpython.com">number is </a> 
                                        hallo.
                                  </p>
                                </body>
                              </html>
                              """

                        # Turn these into plain/html MIMEText objects
                        part1 = MIMEText(text, "plain")
                        # part2 = MIMEText(html, "html")

                        # Add HTML/plain-text parts to MIMEMultipart message
                        # The email client will try to render the last part first
                        message.attach(part1)
                        # message.attach(part2)

                        # Create secure connection with server and send email
                        context = ssl.create_default_context()
                        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                            server.login(sender_email, password)
                            server.sendmail(
                                sender_email, receiver_email, message.as_string()
                            )
                        session['email1'] = email1
                        session['number2'] = number2
                        return redirect(url_for("numberforlosspassword"))
                    else:
                       return render_template("losspassword.html", mserrorlosspasswod2="the mail is or berth not exist")
        else:
            return render_template("losspassword.html", mserrorlosspasswod2="the mail is or berth not exist")

    else:
        return render_template("losspassword.html")


@app.route("/numberforlosspassword", methods=["POST", "GET"])
def numberforlosspassword():
    if request.method == "POST":
        number2 = session.get('number2')
        number3 = request.form["numberx"]
        if number3 == str(number2):
            return render_template("newpassword.html")

        else:
            return render_template("numberforlosspassword.html", mserrornumberconfirms="number error")

    else:
        return render_template("numberforlosspassword.html")


@app.route("/newpassword", methods=["POST", "GET"])
def newpassword():
    if request.method == "POST":
        newpassword = request.form["newpassword"]
        confirms = request.form["confirms"]
        email1 = session.get('email1')
        userandpass = {

        }
        n = 0
        m = 0
        o = 0
        p = 0
        alpha_array = ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'q',
                       'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'z',
                       'x', 'c', 'v', 'b', 'n', 'm']
        capital_array = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                         'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O',
                         'P', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
        symbol_array = ["!", "@", "#", "$", "%", "^", "&", "*",
                        "(", ")", "-", "_", "=", "+", "{", "}",
                        ":", ";", "<", ">", "?", ".", "/", ",", "|"]
        number_array = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

        if len(newpassword) <= 9:
            return render_template("newpassword.html", mserrorpassword1="password error")

        else:
            for x in newpassword:  # check password
                for x4 in number_array:
                    if x4 == x:
                        p += 1
                for x3 in symbol_array:
                    if x3 == x:
                        o += 1
                for x2 in capital_array:
                    if x == x2:
                        m += 1
                for x1 in alpha_array:
                    if x == x1:
                        n += 1
            if n == 0 or m == 0 or p == 0:
                return render_template("newpassword.html", mserrorpassword1="password error")
        if newpassword != confirms:
            return render_template("newpassword.html", mspassworderror="password and confirms not equal")

        import mysql.connector
        import random
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="#password for database",
            database="#databasename"
        )
        mycursor = mydb.cursor()
        n = "SELECT email FROM profile"
        q = "UPDATE profile SET password=%s WHERE email=%s"
        w = "SELECT firstname FROM profile WHERE email=%s"
        mycursor.execute(n)
        myresult = mycursor.fetchall()
        for x in myresult:
            if x == (email1,):
                import mysql.connector
                import random
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="#password for database",
                    database="#databasename"
                )
                mycursor = mydb.cursor()
                n = "SELECT email FROM profile"
                q = "UPDATE profile SET password=%s WHERE email=%s"
                w = "SELECT firstname FROM profile WHERE email=%s"
                mycursor.execute(n)
                myresult = mycursor.fetchall()
                for x in myresult:
                    if x == (email1,):
                        mycursor.execute(w, (email1,))
                        name = mycursor.fetchone()
                        val = (newpassword, email1)
                        mycursor.execute(q, val)
                        mydb.commit()
                        return redirect(url_for("user", usr=name))
    else:
        return render_template("newpassword.html")


if __name__ == '__main__':
    app.run(port=2001, debug=True)
