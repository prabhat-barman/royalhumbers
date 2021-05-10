import os
import random

from flask import *
from flask_mail import Mail, Message
from flaskext.mysql import MySQL
from tkinter import messagebox

app = Flask(__name__)

# database configuration
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'website'
mysql: MySQL = MySQL(app)

# email configuration
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ashubarman98@gmail.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_PASSWORD'] = 'ashuprabhat98'
mail = Mail(app)

# pic configuration
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/img"

app.secret_key = 'ads453'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/send', methods=['POST'])
def send():
    userN = request.form['name']
    em = request.form['email']
    msg = request.form["message"]
    num = request.form['number']
    cursor = mysql.get_db().cursor()
    info = [userN, em, msg, num]
    cursor.execute('INSERT INTO contact (name,email,msg,num)VALUES (%s,%s,%s,%s);', info)
    msg = Message('Hello', sender='ashubarman98@gmail.com', recipients=["prabhatbarman98@gmail.com"],
                  body=str(info))
    mail.send(msg)

    return "done"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/event')
def event():
    cur = mysql.get_db().cursor()
    cur.execute("select * from event ")
    data = cur.fetchall()
    return render_template("event.html", data=data)


@app.route('/sign_up')
def sign_up():
    return render_template("register.html")


@app.route('/profile')
def profile():
    sno = request.args.get('sno')
    info = [sno, ]
    cur = mysql.get_db().cursor()
    cur.execute("select * from worker where sno=%s", info)
    data = cur.fetchall()

    return render_template("profile.html", data=data)


@app.route("/register", methods=['POST'])
def register():
    userN = request.form['name']
    mal = request.form['email']
    work = request.form['work']
    num = request.form['number']
    add = request.form['add']
    des = request.form['Description']
    pic = request.files['photo']
    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
    photo = pic.filename
    cur = mysql.get_db().cursor()
    info = [userN, mal, num, work, add, des, photo]
    cur.execute(
        "INSERT INTO worker (name,email,number,position,address,Description,photo)VALUES (%s,%s,%s,%s,%s,%s,%s);",
        info)

    return "done"


@app.route("/Real_Estate", methods=['POST'])
def RE():
    userN = request.form['name']
    mal = request.form['email']
    work = request.form['work']
    num = request.form['number']
    add = request.form['add']
    des = request.form['Description']
    pic = request.files['photo']
    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
    photo = pic.filename
    cur = mysql.get_db().cursor()
    info = [userN, mal, num, work, add, des, photo]
    cur.execute(
        "INSERT INTO worker (name,email,number,position,address,Description,photo)VALUES (%s,%s,%s,%s,%s,%s,%s);",
        info)

    return "done"


@app.route('/shop')
def shop():
    cur = mysql.get_db().cursor()
    cur.execute("select * from worker where position='shop'")
    data = cur.fetchall()

    return render_template('shop.html', data=data)


@app.route('/realEstate')
def realEstate():
    cur = mysql.get_db().cursor()
    cur.execute("select * from worker where position='Real_Estate'")
    data = cur.fetchall()

    return render_template('shop.html', data=data)


@app.route('/service')
def service():
    search = request.args.get('search')
    info = [search, ]
    cur = mysql.get_db().cursor()
    cur.execute("select * from worker where position=%s", info)
    data = cur.fetchall()

    return render_template('service.html', data=data)


@app.route('/shop2')
def shop2():
    search = request.args.get('search')
    info = [search, ]
    cur = mysql.get_db().cursor()
    cur.execute("select * from worker where address=%s", info)
    data = cur.fetchall()

    return render_template('service.html', data=data)


@app.route("/real_Estate")
def email():
    return render_template("email.html")


@app.route("/auth", methods=["POST"])
def auth():
    email = request.form["email"]
    data = [email, ]
    if data:
        session['user'] = data
        session['otp'] = random.randint(1000, 9999)
        OTP = session['otp']
        mail.init_app(app)
        msg = Message('Hello', sender='ashubarman98@gmail.com', recipients=[session['user'][0]])
        mailcontent = "Your otp is : ", str(OTP)
        msg.body = str(mailcontent)
        mail.send(msg)
        return render_template('otplogin.html')
    else:
        return redirect('/real_Estate')


@app.route('/otp', methods=['POST'])
def otp():
    otpnum = str(request.form['otpnum'])
    if otpnum == str(session['otp']):
        return redirect("/dashboard")
    else:
        return redirect('/logout')


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('realEstate.html')
    else:
        return redirect('/real_Estate')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/real_Estate')


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/upload")
def upload_gallery():
    return render_template("uploadEvent.html")


@app.route('/upload2' , methods=["POST"])
def gallery():
    name = request.form['name']
    pic = request.files['photo']
    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
    photo = pic.filename
    cur = mysql.get_db().cursor()
    info = [name, photo]
    cur.execute(
        "INSERT INTO event (name,photo)VALUES (%s,%s);",
        info)

    return "done"

@app.route('/deleteemp', methods=['GET'])
def deleteemp():
    number = request.args['number']
    cur = mysql.get_db().cursor()
    info = [number,]
    cur.execute(
        "delete from worker where number=%s;",
        info)

    messagebox.showinfo("showinfo", "deleted")

    return redirect('/delete_w')


@app.route("/delete_w")
def delete():
    return render_template("delete.html")

@app.route('/deleteState', methods=['GET'])
def deleteemp1():
    number = request.args['number']
    cur = mysql.get_db().cursor()
    info = [number,]
    cur.execute(
        "delete from pro_ven where number=%s;",
        info)

    messagebox.showinfo("showinfo", "deleted")

    return redirect('/delete_e')


@app.route("/delete_e")
def deleteE():
    return render_template("delete_E.html")
@app.route("/donation")
def donation():
    return render_template("donate.html")
@app.route("/donate",methods=['POST'])
def donate():
    userN = request.form['name']
    mal = request.form['email']
    num = request.form['number']
    add = request.form['add']
    des = request.form['Description']
    pic = request.files['photo']
    pic.save(os.path.join(app.config['UPLOAD_FOLDER'], pic.filename))
    photo = pic.filename
    cur = mysql.get_db().cursor()
    info = [userN, mal, num, add, des, photo]
    cur.execute('INSERT INTO donate (name,email,number,address,Description,photo)VALUES (%s,%s,%s,%s,%s,%s);',
        info)
    msg = Message('Hello', sender='ashubarman98@gmail.com', recipients=["prabhatbarman98@gmail.com"],
                  body=str(info))
    mail.send(msg)

    return "done"



app.run(debug=True, port=1115)
