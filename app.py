from flask import Flask, render_template, request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_Created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def Hello_World():
    title = ""  # Initialize 'title' and 'desc' to avoid UnboundLocalError
    desc = ""
    
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        # Delete rows where title is 'Old Task'
        db.session.query(Todo).filter(Todo.title == '').delete()
        db.session.commit()
        print("Matching Todo items deleted successfully!")

        
    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def Products():
    allTodo = Todo.query.all()
    return 'This is products page'
@app.route('/update')
def update():
    allTodo = Todo.query.all()
    return 'This is products page'
@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()  # Fetch the Todo item by sno
    
    if todo:
        db.session.delete(todo)  # Delete the fetched Todo item
        db.session.commit()  # Commit the changes to the database
        print(f"Todo with sno {sno} deleted successfully!")
    else:
        print(f"Todo with sno {sno} not found!")
    
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
