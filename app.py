from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from models import db, Account
from utils import export_to_excel, export_to_pdf, get_static_path

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    account_number = request.form['account_number']
    phone = request.form['phone']
    deposit_amount = request.form['deposit_amount']
    new_account = Account(name=name, account_number=account_number, phone=phone, deposit_amount=deposit_amount)
    db.session.add(new_account)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/view')
def view():
    accounts = Account.query.all()
    return render_template('view_data.html', accounts=accounts)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    account = Account.query.get_or_404(id)
    if request.method == 'POST':
        account.name = request.form['name']
        account.account_number = request.form['account_number']
        account.phone = request.form['phone']
        account.deposit_amount = request.form['deposit_amount']
        db.session.commit()
        return redirect(url_for('view'))
    return render_template('edit.html', account=account)

@app.route('/delete/<int:id>')
def delete(id):
    account = Account.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return redirect(url_for('view'))

@app.route('/export/excel')
def export_excel():
    accounts = Account.query.all()
    file_path = export_to_excel(accounts)
    return send_file(file_path, as_attachment=True)

@app.route('/export/pdf')
def export_pdf():
    accounts = Account.query.all()
    file_path = export_to_pdf(accounts)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
