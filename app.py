from flask import Flask,render_template,request,url_for,session,redirect,flash
from flask_mysqldb import MySQL
app=Flask(__name__,template_folder='template')
app.secret_key="123"
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="library01"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


# admin logout

@app.route("/logout")
def logout():
    return redirect(url_for("admin"))

#-------home page-----------
@app.route("/")
def index():
    return render_template('index.html')


#-------admin dashboard-------
@app.route("/admin_dash")
def admin_dash():
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
                    return redirect(url_for('admin_dash'))
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
                    return redirect(url_for('student_dash'))
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
def student_dash():
    return render_template("student_dash.html")

#---------admin_dash_book_availability------
@app.route("/bookdb",methods=['POST','GET'])
def bookdb():
    if 'submit' in request.form:
        if request.method == 'POST':
            bname= request.form["bname"]
            author= request.form["author"]
            try:
                cur=mysql.connection.cursor()
                print("success")
                cur.execute("select * from bookdatabase where bname=%s and author=%s",[bname,author])
                res= cur.fetchone()
                print(res)
                if res and res['bname']==bname and res['author']==author:
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
def bookdbs():
    if 'submit' in request.form:
        if request.method == 'POST':
            bname = request.form["bname"]
            author = request.form["author"]
            try:
                cur = mysql.connection.cursor()
                print("success")
                email=session["email"]
                print("Working fine",email)
                cur.execute("insert into bookreserve (email,book,author,`date&time`) values(%s,%s,%s,now())", [email,bname,author])
                flash("BOOKING SUCCCESSFULL")
                cur.execute("update bookdatabase set quantity=GREATEST(quantity-1,0) where bname=%s and author=%s",[bname,author])

            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()
    return render_template("student_dash.html",show_reserve=True)

#-------------student_dash _book_availability
@app.route("/bookdbse",methods=['POST','GET'])
def bookdbse():
    if 'submit' in request.form:
        if request.method == 'POST':
            bname= request.form["bname"]
            author= request.form["author"]
            try:
                cur=mysql.connection.cursor()
                print("success")
                cur.execute("select * from bookdatabase where bname=%s and author=%s",[bname,author])
                res= cur.fetchone()
                print(res)
                if res and res['bname']==bname and res['author']==author:
                    flash("available")
                else:
                    flash("not available")
            except Exception as e:
                print(e)
            finally:
                mysql.connection.commit()
                cur.close()


    return render_template("student_dash.html")

if __name__=='__main__':
    app.run(debug=True)
