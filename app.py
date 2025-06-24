from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ----------------------- Database Model --------------------------
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_Created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


# ----------------------- Routes --------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    title = ""
    desc = ""
    query = None  # <-- important to initialize it

    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        db.session.query(Todo).filter(Todo.title == '').delete()
        db.session.commit()
    
    query = request.args.get('query')
    if query:
        allTodo = Todo.query.filter(
            (Todo.title.ilike(f"%{query}%")) |
            (Todo.desc.ilike(f"%{query}%"))
        ).all()
    else:
        allTodo = Todo.query.all()

    return render_template('index.html', allTodo=allTodo, query=query)



@app.route('/show')
def show():
    return 'This is products page'


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect('/')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # ✅ Save login attempt to logins.log
        with open("logins.log", "a") as log:
            log.write(f"{datetime.now()} - Email: {email}\n")

        print(f"Login attempt from: {email}")
        return redirect('/')
    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # ✅ Save signup details in signups.log file
        with open("signups.log", "a") as log:
            log.write(f"{datetime.now()} - Username: {username}, Email: {email}\n")

        print(f"Signup saved for: {username} - {email}")
        return redirect('/')
    return render_template('signup.html')

# ----------------------- Main --------------------------

if __name__ == "__main__":
    app.run(debug=True)
