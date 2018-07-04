from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
import time
import statsd
c = statsd.StatsClient('localhost',8125)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, content):
        self.content = content
        self.done = False

    def __repr__(self):
        return '<Content %s>' % self.content


db.create_all()


@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


@app.route('/task', methods=['POST'])
def add_task():
	#start=time.time()
    content = request.form['content']
    if not content:
    	#dur = (time.time() - start) *1000
    	#c.timing("errortime",dur)
    	#c.incr("errorcount")
        return 'Error'
    task = Task(content)
    db.session.add(task)
    db.session.commit()
   # dur = (time.time() - start) *1000
   # c.timing("tasktime",dur)
   # c.incr("taskcount")
    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
    	#c.incr("errorcount")
        return redirect('/')

    db.session.delete(task)
    db.session.commit()
    #c.incr("deletecount")
    return redirect('/')


@app.route('/done/<int:task_id>')
def resolve_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return redirect('/')
    if task.done:
        task.done = False
    else:
        task.done = True

    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
