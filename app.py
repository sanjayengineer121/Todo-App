from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql.expression import select, exists
import hashlib
import webbrowser
app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    Work = db.Column(db.String(500))
    Done = db.Column(db.Boolean)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'Work': self.Work,
            'Done': self.Done
        }
    def __repr__(self) -> str:
        return f'{self.id} - {self.title}'

class adminp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
           'username': self.username,
            'password': self.password
        }
    def __repr__(self) -> str:
        return f'{self.id}'

import os.path
file_exists = os.path.exists('todolist.sqlite')
if file_exists==1:
    pass
else:
    db.create_all()


@app.route("/",methods = ['POST', 'GET'])
def demo():
    todo_details = TODO.query.all()
    return render_template("data1.html", todo_details=todo_details,TODO=TODO)

@app.route("/todos")
def home():
    todo_details = TODO.query.all()
    return render_template("data1.html", todo_details=todo_details,TODO=TODO)

@app.route("/todo")
def home1():
    todo_details = TODO.query.all()
    return render_template("data.html", todo_details=todo_details,TODO=TODO)

@app.route("/login", methods=["POST"])
def logi():
    Username= request.form.get("Username")
    password = request.form.get("password")
    print(Username)
    print(password)

    engine = create_engine('sqlite:///todolist.sqlite')
    Session = sessionmaker(bind=engine)
    import sqlalchemy
        
    session = Session()
    hash1 = hashlib.md5(password.encode("utf-8")).hexdigest()

    s1=session.query(exists().where(admint.username==Username,admint.password==hash1)).scalar()

    if s1==1:
        todo_details = TODO.query.all()
        return render_template("data.html", todo_details=todo_details,TODO=TODO)


@app.route("/signup", methods = ['POST', 'GET'])
def singup():

    return render_template('signup.html')

@app.route("/adddata", methods=["POST"])
def adduser():
    Username= request.form.get("Username")
    password = request.form.get("password")
    password2 = request.form.get("password1")
    print(Username)
    print(password)

    if password==password2:
        hash1 = hashlib.md5(password.encode("utf-8")).hexdigest()

        sale=Login(username=Username,password=hash1)
        db.session.add(sale)
        db.session.commit()

        print("successfully Addes")
        return redirect(url_for("demo"))
    else:
        return "password Not Matched kindly Try Again"

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    Work = request.form.get("Work")
    newdata = TODO(title=title,Work=Work, Done=False)
    db.session.add(newdata)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = TODO.query.filter_by(id=todo_id).first()
    todo.Done = not todo.Done
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update1/<int:todo_id>")
def update1(todo_id):
    todo = TODO.query.filter_by(id=todo_id).first()
    todo.Done = not todo.Done
    db.session.commit()
    return redirect(url_for("home1"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):

    todo = TODO.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home1"))


@app.route('/api/data')
def data():
    return {'data': [TODO.to_dict() for TODO in TODO.query]}

if __name__ == "__main__":
    app.debug=True
    
    url="http://127.0.0.1:"+str(8086)+"/"
    webbrowser.open_new(url)
    app.run(host='0.0.0.0', port=8086)
