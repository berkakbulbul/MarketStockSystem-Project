from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import re

app = Flask(__name__)

app.secret_key = "xd"

try:
    cnx = mysql.connector.connect(user='root',
                                  password='1234',
                                  host='127.0.0.1',
                                  db='projtest')
except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
cursor = cnx.cursor()




@app.route('/')
def test():
    return render_template("firstpage.html")


@app.route('/statistics')
def stats():
    cursor.execute('SELECT * FROM product')
    data = cursor.fetchall()
    mylabels = []
    y = np.empty([len(data)])
    for i in data:
        mylabels.append(i[3])
    str = 'Product Distrubution'
    for i in range(0, len(data)):
        y[i] = data[i][7]

    plt.pie(y, labels=mylabels, startangle=90, autopct='%1.2f%%')
    #plt.legend(loc="upper right")
    plt.title(str)
    plt.savefig('./static/Pie.png')
    plt.clf()


    cursor.execute('SELECT * FROM product')
    data = cursor.fetchall()
    x = []
    y = []
    for i in data:
        x.append(i[2] + i[3])
        y.append(int(i[5]) * int(i[7]))
    plt.rcParams['xtick.major.pad'] = '0.2'
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.bar(x, y, color='brown')
    plt.xticks(rotation=70, horizontalalignment='center')
    plt.ylabel('Income')
    plt.xlabel('Products')
    plt.subplots_adjust(bottom=0.15)
    plt.title('Total Value of Products')
    plt.savefig('./static/Bar.png')
    plt.clf()

    cursor.execute('SELECT * FROM product')
    data = cursor.fetchall()
    x = []
    y = []
    for i in data:
        x.append(i[3])
        y.append(int(i[5]))
    plt.rcParams['xtick.major.pad'] = '0.2'
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.plot(x, y, color='navy')
    plt.xticks(rotation=70, horizontalalignment='center')
    plt.ylabel('Price')
    plt.xlabel('Products')
    plt.subplots_adjust(bottom=0.15)
    plt.title('Price of Products')
    plt.savefig('./static/Plot.png')
    plt.clf()

    cursor.execute('SELECT * FROM record')
    data = cursor.fetchall()
    x = []
    y = []
    for i in data:
        x.append(i[1])
        y.append(int(i[2]) )
    plt.rcParams['xtick.major.pad'] = '0.2'
    plt.rcParams['figure.figsize'] = (10, 8)
    plt.plot(x, y, color='navy')
    plt.xticks(rotation=70, horizontalalignment='center')
    plt.ylabel('Quantity')
    plt.xlabel('Products')
    plt.subplots_adjust(bottom=0.15)
    plt.title('Quantity of Products')
    plt.savefig('./static/Plot.png')
    plt.clf()

    return render_template("statistics.html")


@app.route('/base')
def base():
    return render_template("base.html")


@app.route('/navbar')
def navbar():
    return render_template("navbar.html")


@app.route('/mainpage', methods=['POST', 'GET'])
def mainpage():

    if "m_name" in session:
        m_name = session["m_name"]
        cursor.execute('SELECT * FROM product WHERE marketname = %s', (m_name,))
        fetchdata = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM product")
        fetchdata = cursor.fetchall()

    if request.method == 'POST':
        if request.form['submit_button'] == 'Add to Inventory':
            product_name = request.form.get("p_name")
            category = str(request.form.get("category"))
            brand = str(request.form.get("brand"))
            price = str(request.form.get("price"))
            amount = str(request.form.get("amount"))
            weight = str(request.form.get("weight"))
            print(product_name, category, brand, price, amount,m_name)
            try:
                cursor.execute(
                    "INSERT INTO `product` (`name`,`kind`,`brand`,`price`,`amount`,`weight`,`marketname`) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    (product_name, category, brand, price, amount, weight,m_name))
                cnx.commit()
            except Exception as error:
                print(error)
            return render_template('main.html', data=fetchdata)

        ##### ADD-REMOVE BUTTONs ####
        elif request.form['submit_button'] == 'Add' or request.form['submit_button'] == 'Remove':
            firstid=fetchdata[0][0]
            try:
                for i in range(1, len(fetchdata) + 1):  # Checking the items
                    temp = request.form.get("number" + str(i))
                    if temp != '':  # Eğer boşsa '' görüyor, değilse sayı alabiliriz.
                        itemnum = i+firstid-1
                        number = int(temp)

            except Exception as error:
                print(error)
                return render_template('main.html', data=fetchdata)

            # Getting the previous amount for statistics part
            try:
                cursor.execute(""" SELECT * FROM product WHERE product_id = %s""" % itemnum)
                row = cursor.fetchone()
                previous_amount = row[7]  # Amount numb
                rprice = row[5]  # price for record
                rname = row[3]  # price for record

            except Exception as error:
                print(error)

            ## --- ADD BUTTON --- ##
            if request.form['submit_button'] == 'Add':
                # Updating Query
                try:
                    query = """ UPDATE product SET amount = %s where product_id = %s """
                    new_amount = int(previous_amount) + number
                    cursor.execute(query, (new_amount, itemnum))
                    cnx.commit()
                except Exception as error:
                    print(error)

                try: ##Adding to records
                    cursor.execute(
                        "INSERT INTO `record` (`name`,`amount`,`price`) VALUES (%s,%s,%s)",(rname,number,rprice))
                    cnx.commit()
                except Exception as error:
                    print(error)

            ## --- REMOVE BUTTON --- ##
            else:
                try:
                    if int(previous_amount) < number:
                        return render_template('main.html', data=fetchdata)

                    query = """ UPDATE product SET amount = %s where product_id = %s """
                    new_amount = int(previous_amount) - number
                    cursor.execute(query, (new_amount, itemnum))
                    cnx.commit()
                except Exception as error:
                    print(error)
                try: ##Adding to records
                    number = number * -1
                    cursor.execute("INSERT INTO `record` (`name`,`amount`,`price`) VALUES (%s,%s,%s)",(rname,number,rprice))
                    cnx.commit()
                except Exception as error:
                    print(error)
            return render_template('main.html', data=fetchdata)

    else:
        return render_template('main.html', data=fetchdata)


@app.route('/prebase')
def prebase():
    return render_template("prebase.html")


# login(extends prebase)
@app.route('/login',methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        cursor.execute('SELECT * FROM user WHERE email = %s AND password = %s', (email,password,))
        # Fetch one record and return result
        account = cursor.fetchone()

        try:
            session['user_mail'] = account[5]
        except Exception as error:
            print(error)
            return render_template("login.html", msg=msg)
        session['m_name'] = account[3]

        if account:
            #return 'Logged in successfully!'
            return redirect(url_for("mainpage"))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template("login.html", msg=msg)

@app.route('/logout')
def logout():
    return redirect(url_for("login"))


# signup(extends prebase)
@app.route('/register',methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'surname' in request.form and 'marketname' in request.form and 'email' in request.form and 'password' in request.form:
        # Create variables for easy access
        name = request.form['name']
        surname = request.form['surname']
        marketname = request.form['marketname']
        email = request.form['email']
        password = request.form['password']

        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', surname):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[A-Za-z0-9]+', marketname):
            msg = 'Username must contain only characters and numbers!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not name or not surname or not marketname or not email or not password :
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO user VALUES (NULL,%s,%s,%s,NULL, %s, %s,NULL,NULL,NULL)',
                           (name,surname,marketname,email, password,))
            cnx.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
        # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/retailers')
def retailers():
    cursor.execute("SELECT * FROM retailer")
    retailer_data = cursor.fetchall()
    return render_template("retailers.html",data=retailer_data)

@app.route('/profile')
def profile():
    user_mail = session["user_mail"]
    cursor.execute('SELECT * FROM user WHERE email = %s', (user_mail,))
    user_data = cursor.fetchone()
    print(user_data)
    if request.method == 'POST':
        return redirect(url_for("profileupdate"))
    return render_template("profile.html", user_data=user_data)

@app.route('/profileupdate',methods=['GET', 'POST'])
def profileupdate():
    if request.method == 'POST':
        username = request.form.get("username")
        usersurname = request.form.get("usersurname")
        userpassword = request.form.get("userpassword")
        userphone = request.form.get("userphone")
        user_mail = session["user_mail"]
        print(user_mail)
        try:
            query = """ UPDATE user SET name = %s, surname = %s, phone = %s, password = %s where email = %s """

            cursor.execute(query, (username, usersurname,userphone ,userpassword ,user_mail))
            cnx.commit()
            return redirect(url_for("profile"))
        except Exception as error:
            print(error)
    return render_template("profileupdate.html")