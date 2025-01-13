from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(50), nullable=False)


def reset_database():
    with app.app_context():
        db.drop_all()  
        db.create_all() 


@app.route('/')
def index():
    transactions = Transaction.query.all()
    total_income = sum(t.amount for t in transactions if t.amount > 0)
    total_expense = sum(t.amount for t in transactions if t.amount < 0)
    balance = total_income + total_expense
    return render_template('index.html', transactions=transactions, 
                           total_income=total_income, total_expense=total_expense, balance=balance)


@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        title = request.form['title']
        amount = float(request.form['amount'])
        category = request.form['category']
        
     
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()

        new_transaction = Transaction(title=title, amount=amount, date=date, category=category)
        db.session.add(new_transaction)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('add.html')


if __name__ == '__main__':
    reset_database() 
    app.run(debug=True)
