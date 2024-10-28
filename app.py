
from flask import Flask,render_template,request,url_for,session,redirect,flash,jsonify,make_response
from flask_mysqldb import MySQL
from flask_mail import Mail,Message
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_wtf import CSRFProtect
from flask_jwt_extended import create_access_token, set_access_cookies,jwt_required,get_jwt_identity,unset_jwt_cookies,JWTManager
from flask_jwt_extended.exceptions import NoAuthorizationError




app=Flask(__name__,template_folder='template')
app.secret_key="123"
csrf=CSRFProtect(app)
app.config['WTF_CSRF_COOKIE_SECURE']=True
app.config['JWT_SECRET_KEY'] = "45645"
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
jwt=JWTManager(app)
#mail_config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']='465'
app.config['MAIL_USERNAME']=''
app.config['MAIL_PASSWORD']='ibek ihkc kdeh akne'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
#database config
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="library01"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)







def check_due_remainder():
    with app.app_context():
        cur = mysql.connection.cursor()
        today = datetime.date.today()
        cur.execute("SELECT email, book, `date&time` FROM bookreserve WHERE DATE(`date&time`) + INTERVAL 12 DAY = %s and email_sent=FALSE ", (today,))
        rows = cur.fetchall()

        for row in rows:
            email = row['email']
            book = row['book']
            reserve_date = row['date&time']

            # Create the email message
            msg = Message("Reminder: Return your reserved book", sender='noreply@demo.com', recipients=[email])
            msg.body = f"Dear {email}, please return the book '{book}' reserved on {reserve_date} within the next 3 days."

            # Send the email
            mail.send(msg)
            cur.execute("update bookreserve set email_sent=TRUE where email=%s and `date&time`=%s",(email,reserve_date))
            print(f"Reminder email sent to {email}")

        mysql.connection.commit()
        cur.close()

# Scheduler job to run every minute
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_due_remainder, trigger="interval", minutes=1)

# Start the scheduler
scheduler.start()

@app.errorhandler(NoAuthorizationError)
def handle_error(e):
    return jsonify({"msg":"invaild authorization"}),401
# admin logout

@app.route("/logout_admin")
def logout_admin():
    session.clear()
    print(session)
    response=make_response(redirect(url_for('admin')))
    unset_jwt_cookies(response)
    return response

@app.route("/logout_student")
def logout_student():
    session.clear()
    print(session)
    response=make_response(redirect(url_for('index')))
    unset_jwt_cookies(response)
    return response

#-------home page-----------
@app.route("/")
def index():
    return render_template('index.html')

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route("/index1")
def index1():
    return render_template('index.html')

#-------admin dashboard-------
@app.route("/admin_dash")
@jwt_required()
def admin_dash():
    current_user=get_jwt_identity()
    print(f"Current user: {current_user}")
    return render_template("admin_dash.html")

#------admin login page-------
@app.route("/admin",methods=['GET','POST'])
def admin():
    if 'submit' in request.form:
        if request.method == 'POST':
            email = request.form["email"]
            password = request.form["password"]
            try:
                cur = mysql.connection.cursor()
                print("success")
                cur.execute("select * from admin where email=%s and password=%s", [email, password])
                res = cur.fetchone()
                if res:
                    access_token=create_access_token(identity=email)
                    response=make_response(redirect(url_for('admin_dash')))
                    set_access_cookies(response,access_token)
                    return response
                else:
                    return render_template('adminlogin.html', error="invalid email or password")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template('adminlogin.html')

#-----------student login page---------
@app.route("/student",methods=['POST','GET'])
def student():
    if 'submit' in request.form:
        if request.method == 'POST':
            email = request.form["email"]
            password = request.form["password"]
            try:
                cur = mysql.connection.cursor()
                print("success")
                cur.execute("select * from student where email=%s and password=%s", [email, password])
                res = cur.fetchone()
                if res:
                    session["email"]=res["email"]
                    print(session)
                    access_token = create_access_token(identity=email)
                    response = make_response(redirect(url_for('student_dash')))
                    set_access_cookies(response, access_token)
                    print(access_token)
                    return response
                else:
                    return render_template('index.html',error="invalid email or password")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template('index.html')

#--------student_dash------------
@app.route("/student_dash")
@jwt_required()
def student_dash():
    current_user=get_jwt_identity()
    print(f"Current user: {current_user}")
    return render_template("student_dash.html")

#---------admin_dash_book_availability------
@app.route("/bookdb",methods=['POST','GET'])
def bookdb():
    if 'submit' in request.form:
        if request.method == 'POST':
            bname= request.form["bname"]
            author= request.form["author"]
            isbn= request.form["isbn"]
            try:
                cur=mysql.connection.cursor()
                print("success")
                cur.execute("select * from bookdatabase where bname=%s and author=%s and isbn=%s",[bname,author,isbn])
                res= cur.fetchone()
                print(res)
                if res and res['bname']==bname and res['author']==author and res['isbn']==isbn:
                    flash("available")
                else:
                    flash("not available")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()


    return render_template("admin_dash.html")

#-------student_dash _book_reservation--------
@app.route("/bookreserve",methods=['POST','GET'])
def bookreserve():
    if 'submit' in request.form:
        if request.method == 'POST':
            bname = request.form["bname"]
            author = request.form["author"]
            isbn = request.form["isbn"]
            try:
                cur = mysql.connection.cursor()
                print("success")
                email=session["email"]
                print("Working fine",email)
                cur.execute("select * from bookdatabase where bname=%s and author=%s and isbn=%s", [bname, author,isbn])
                res = cur.fetchone()
                print(res)
                if res and res['bname'] == bname and res['author'] == author and res['isbn'] == isbn and res['quantity']>0:
                    cur.execute("insert into bookreserve (email,book,author,isbn,`date&time`) values(%s,%s,%s,%s,now())",
                                [email, bname, author,isbn])
                    flash("BOOKING SUCCCESSFULL")
                    cur.execute("update bookdatabase set quantity=GREATEST(quantity-1,0) where bname=%s and author=%s and isbn=%s",
                                [bname, author,isbn])
                else:
                    flash("OUT OF STOCK")


            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template("student_dash.html",show_reserve=True)

#-------------student_dash _book_availability
@app.route("/bookdbse",methods=['POST','GET'])
def bookdbse():
    if request.method == 'POST':
        if 'submit' in request.form:
            bname = request.form["bname"]
            author = request.form["author"]
            isbn = request.form['isbn']
            try:
                cur = mysql.connection.cursor()
                print("success")
                cur.execute("select * from bookdatabase where bname=%s and author=%s and isbn=%s", [bname, author,isbn])
                res = cur.fetchone()
                print(res)
                if res and res['bname'] == bname and res['author'] == author and res['isbn'] == isbn and res['quantity'] > 0:
                    flash("available")
                else:
                    flash("not available")
                    return render_template("student_dash.html", show_email=True, bname=bname, author=author, isbn=isbn)
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
        elif 'yes' in request.form:
            email = request.form["email"]
            book = request.form["bname"]
            author = request.form["author"]
            isbn =request.form["isbn"]
            try:
                cur = mysql.connection.cursor()
                print("success")
                cur.execute("insert into emailnotice (email,book,author,isbn) values(%s,%s,%s,%s)", (email, book, author,isbn))

                flash("will notify when updated")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template("student_dash.html")
#------student book_list
@app.route("/booklistse")
def booklistse():
    cur=mysql.connection.cursor()
    print("success")
    cur.execute(" select * from bookdatabase")
    result=cur.fetchall()
    print("s")
    print(result)
    print("s")
    cur.close()
    return render_template("student_dash.html",show_list=True,results=result)

#------admin book list-------
@app.route("/booklist")
def booklist():
    cur=mysql.connection.cursor()
    print("success")
    cur.execute(" select * from bookdatabase")
    result=cur.fetchall()
    print("s")
    print(result)
    print("s")
    cur.close()
    return render_template("admin_dash.html",show_list=True,results=result)

#-----student book return-----
@app.route("/bookreturn",methods=['GET','POST'])
def bookreturn():
    if 'submit' in request.form:
        if request.method=='POST':
            bname=request.form["bname"]
            author=request.form["author"]
            isbn=request.form["isbn"]
            try:
                cur=mysql.connection.cursor()
                email=session["email"]
                cur.execute("insert into bookreturn (email,book,author,isbn,`date&time`,status) values(%s,%s,%s,%s,now(),%s)",(email,bname,author,isbn,'Pending'))

                if cur.rowcount>0:
                    flash("request sent successfully")
                else:
                    flash("Unsuccessfull")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template("student_dash.html",show_return="True")

#----------------admin request handling---------
@app.route("/return_list")
def admin_dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bookreturn WHERE status='Pending'")
    requests = cur.fetchall()
    print(requests)
    cur.close()
    return render_template("admin_dash.html", requests=requests,return_list=True)


@app.route("/accept_request", methods=['POST'])
def accept_request():
    request_id = request.form.get("request_id")

    cur = mysql.connection.cursor()
    cur.execute("select email,book,author,isbn from bookreturn where email=%s",[request_id])
    book_data=cur.fetchone()
    if book_data:
        email,bname,author,isbn=book_data['email'],book_data['book'],book_data['author'],book_data['isbn']
        cur.execute("UPDATE bookreturn SET status='Accepted' WHERE email=%s", [request_id])
        cur.execute("update bookdatabase set quantity=GREATEST(quantity+1,0) where bname=%s and author=%s and isbn=%s",
                    [bname, author,isbn])
        cur.execute("update bookreserve set email_sent=TRUE where email=%s and isbn=%s", (email,isbn))
        cur.execute("select email from emailnotice where book=%s and author=%s",[bname,author])
        res=cur.fetchall()
        if res:

            mail_notice=[row['email'] for row in res]
            msg = Message("hey", sender='noreply@demo.com', recipients=mail_notice)
            msg.body = " book was returned to library , you can collect it"
            mail.send(msg)
            print("mail success")
            cur.executemany("delete from emailnotice where email=%s",[(email,) for email in mail_notice])


    mysql.connection.commit()
    cur.close()

    return render_template("admin_dash.html", return_list=True)


@app.route("/decline_request", methods=['POST'])
def decline_request():
    request_id = request.form.get("request_id")

    cur = mysql.connection.cursor()
    cur.execute("UPDATE bookreturn SET status='Declined' WHERE email=%s", [request_id])
    mysql.connection.commit()
    cur.close()


    return render_template("admin_dash.html", return_list=True)


if __name__=='__main__':
    with app.app_context():
        app.run(debug=True)

