import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=True)
    money = db.Column(db.Float, nullable=True)

class Expences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(50), nullable=True)
    money = db.Column(db.Float, nullable=True)


@app.route('/')
@app.route('/home')
def index():
    incomes = Income.query.all()
    total_income = 0
    for income in incomes:
        total_income += income.money

    expences = Expences.query.all()
    total_expences = 0
    for expence in expences:
        total_expences += expence.money

    total_money = total_income - total_expences

    total_expence_percent = 0
    if total_income != 0:
        total_expence_percent = total_expences / total_income * 100

    date = datetime.utcnow()
    date = date.strftime("%B")



    return render_template("index.html", incomes=incomes, expences=expences,total_income=total_income,
                           total_expences=total_expences, total_money=total_money,
                           total_expence_percent=total_expence_percent, date=date)




@app.route('/submit', methods=['POST', 'GET'])
def submit():

    if request.method == "POST":
        choice = request.form['Operations']
        description = request.form['description']
        money = request.form['total_money']

        if choice == 'inc':
            income = Income(description=description, money=money)
            db.session.add(income)
            db.session.commit()
        elif choice == 'exp':
            expences = Expences(description=description, money=money)
            db.session.add(expences)
            db.session.commit()


    return redirect(url_for('index'))


@app.route('/delete_exp/<int:id>')
def delete_exp(id):
    expence_to_delete = Expences.query.get(id)
    db.session.delete(expence_to_delete)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete_inc/<int:id>')
def delete_inc(id):
    income_to_delete = Income.query.get(id)
    db.session.delete(income_to_delete)
    db.session.commit()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
