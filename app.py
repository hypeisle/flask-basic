from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os  # Import the os module


app = Flask(__name__)

# Get the absolute path of the directory where the script is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Configure the database URI using a relative path
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "test.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional: Disables modification tracking to avoid warnings
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    # return render_template('index.html')
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task.'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task.'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task.'

    else:
        return render_template('update.html', task=task)



if __name__ == "__main__":
    try:
        with app.app_context():
            print(f"Current working directory: {os.getcwd()}")
            print("Attempting to create the database...")
            db.create_all()  # Creates the database tables
            print("Database created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

    app.run(debug=True)
