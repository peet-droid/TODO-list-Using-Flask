from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
        sno = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        description = db.Column(db.String(500), nullable=False)
        data_created = db.Column(db.DateTime, default = datetime.utcnow)

        def __repr__(self):
                return f"{self.description} - {self.title}"

@app.route("/", methods=['GET', 'POST'])

def hello():
        if request.method == 'POST':
                title = request.form['title']
                desc = request.form['desc']
                todo = Todo(title=title,description=desc)
                db.session.add(todo)
                db.session.commit()
                print(todo)
        alltodo = Todo.query.all()
        print(alltodo)
        return render_template('index.html',alltodo=alltodo)

@app.route("/delete/<int:sno>")

def delete(sno):
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")

if __name__ == "__main__":
        app.run(debug=True)