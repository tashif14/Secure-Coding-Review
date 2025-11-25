from flask import Flask,render_template,request,redirect,session
import sqlite3


conn = sqlite3.connect("sql.db")

app = Flask(__name__)
app.secret_key = 'b3c388d053131159dd18c776a75d03ec'
app.config['MAX_LOGIN_ATTEMPTS'] = 5

@app.route("/")

def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    if 'user' not in  session:
            return redirect("/login")
    user = session.get('user')            # username or None
    user_id = session.get('user_id') 

    return render_template("dashboard.html", user=user, user_id=user_id)

@app.route("/greeting", methods=["GET","POST"])

def greeting():
    if request.method == "POST":
        name = request.form.get("name")
        return render_template("greeting.html", name=name)
    return render_template("greeting.html")

@app.route("/xss", methods=["POST", "GET"])

def xss():
    if request.method == "GET":

        fname = request.args.get("input")
    return render_template("xss.html", input=fname)



@app.route("/register", methods=["GET","POST"])

def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        print("username",username, "password",password)
        #create database
        conn = sqlite3.connect("sql.db")
        
        ins = f''' insert into sample5 (username,password,email) VALUES ('{username}','{password}','{email}') '''

        
        conn.execute(ins)
        conn.commit()
        print("Record inserted successfully")
        conn.close()

        return redirect("/login")



    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])

def login():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        
        # Check if the user is locked out
        if 'login_attempts' in session and session['login_attempts'] >= app.config['MAX_LOGIN_ATTEMPTS']:
            return 'Account locked. Please try again later.'

        conn = sqlite3.connect("sql.db")
        query = f" select * from sample5 WHERE username = '{username}' AND password = '{password}'"
        result = conn.execute(query).fetchone()
        # conn.close()

       
        if result:
            print("you are in resul")
        
            session['user'] = username
            session['user_id'] = result[0]  # Store user ID in session

            return redirect("/dashboard")
        else :

            # Update login attempts
            if 'login_attempts' in session:
                session['login_attempts'] += 1
            else:
                session['login_attempts'] = 1
            return redirect("/login")
        
    return render_template("login.html")

@app.route("/profile/<id>", methods=["GET","POST"])
def profile(id):
    if request.method == "GET":
        if 'user' not in  session:
            return redirect("/login")
    
        conn = sqlite3.connect("sql.db")
        user = conn.execute("SELECT * FROM sample5 WHERE id = ?", (id,)).fetchone()
        conn.close()
        
        
    return render_template("profile.html", user=user)
@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)

