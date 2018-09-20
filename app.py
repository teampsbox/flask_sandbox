import os
from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(25), index=True, nullable=False)
    last_name = db.Column(db.String(25), index=True, nullable=False)

    def __repr__(self):
        return '<Client %r>' % self.first_name


class ClientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ClientForm()
    clients = Client.query.all()
    if form.validate_on_submit():
        client = Client(first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(client)
        db.session.commit()
        flash('Client successfully added!')
        return redirect('/')
    return render_template('index.html', clients=clients, form=form)


if __name__ == '__main__':
    app.run()
