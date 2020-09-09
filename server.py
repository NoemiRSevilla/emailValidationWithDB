from flask import Flask, render_template, request, redirect, flash
from mysqlconnection import connectToMySQL
import re

app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe' 

@app.route("/")
def index():
    return render_template ("index.html")

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
@app.route("/", methods=["POST"])
def addEmailToDB():
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
        is_valid=False
        flash("<div class='ohno'>Invalid email addres</div>")
    if len(request.form['email'])<1:
        is_valid = False
        flash("<div class='ohno'>Please enter email</div>")
    if not is_valid: 
        return redirect('/')
    else:
        mysql=connectToMySQL("emailsdb")
        query = "INSERT INTO emails (email, created_at) VALUES (%(email)s, NOW());"
        data ={
            "email": request.form['email'],
        }
        new_email_id=mysql.query_db(query, data)
        return redirect ('/success')

@app.route("/success")
def showEmailToDB():
    first_name= session["first_name"],
    return render_template("show.html", first_name=first_name)

if __name__ == "__main__":
    app.run(debug=True)