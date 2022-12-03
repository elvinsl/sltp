from flask import Flask, render_template, url_for, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '074b6bd219f80cd2a161af1cb15e3a80'


class MainForm(FlaskForm):
    entry_number = FloatField('Entry', validators=[DataRequired()])
    submit_long = SubmitField('Enter Long')
    submit_short = SubmitField('Enter Short')


def calc_long(entry_data):
    stop_loss = entry_data * 0.996
    target_profit = entry_data * 1.005
    return round(stop_loss, 2), round(target_profit, 2)


def calc_short(entry_data):
    stop_loss = entry_data * 1.004
    target_profit = entry_data * 0.995
    return round(stop_loss, 2), round(target_profit, 2)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()
    if form.validate_on_submit():
        submit_data = 'Long Position' if form.submit_long.data else 'Short Position'
        category = 'success' if form.submit_long.data else 'danger'
        stop_loss, target_profit = calc_long(form.entry_number.data) \
                                   if submit_data == 'Long Position' \
                                   else calc_short(form.entry_number.data)
        flash(f'You entered {submit_data}', category=category)
        flash(f'Your Stop Loss : {stop_loss}', category=category)
        flash(f'Your Target Profit : {target_profit}', category=category)
    return render_template('index.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
