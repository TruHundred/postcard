# Импортирование библиотек
from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.recaptcha import validators
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:15931@localhost/my_database'
db = SQLAlchemy(app)
Bootstrap(app)
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LenfaspAAAAAMyLuQb9EXsZwQAkSy6Ybm3m8lqn'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LenfaspAAAAAJDLrPwi2hDCst2LWHOxkylM4Cq9-'


# Создает поля для базы данных
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(500), nullable=False)


# Создает форму для базы данных
class FeedbackForm(FlaskForm):
    name = StringField('Ваше имя', validators=[DataRequired()])
    email = StringField('Ваша почта', validators=[DataRequired()])
    message = StringField('Сообщение', validators=[DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Отправить')


# Функция для отображения главной страницы
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Домашняя страница")


# Функция для отображения страницы с примерами
@app.route('/examples')
def examples():
    return render_template('examples.html', title="Примеры работ")


# Функция для отображения страницы обратной связи
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        feedback = Feedback(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback submitted successfully!')
    return render_template('feedback.html', form=form, title="Обратная связь")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# Запуск приложения
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
