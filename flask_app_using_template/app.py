from flask import Flask,render_template,url_for,request,flash,redirect
import os

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("home.html",)



app.secret_key = "Secret Key"

# SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/student'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Creating model table for our CRUD database
class Employees(db.Model):
    id = db.Column('employee_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    salary = db.Column(db.Float(50))
    age = db.Column(db.String(200))
    pin = db.Column(db.String(10))

    def __init__(self, name, salary, age, pin):
        self.name = name
        self.salary = salary
        self.age = age
        self.pin = pin

@app.route('/view')
def list_employees():
    return render_template('list_employee.html', Employees=Employees.query.all())


@app.route('/add', methods=['GET', 'POST'])
def addEmployee():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['salary'] or not request.form['age']:
            flash('Please enter all the fields', 'error')
        else:
            employee = Employees(request.form['name'], request.form['salary'],request.form['age'], request.form['pin'])

            db.session.add(employee)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('list_employees'))
    return render_template('add.html')
db.create_all()



    # # This route is for deleting our employee
@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = Employees.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employee Deleted Successfully")
    return redirect(url_for('list_employees'))



@app.route('/pic', endpoint='func1')
def student():
   return render_template('show.html')

if __name__ == '__main__':
    app.run(debug=True)
