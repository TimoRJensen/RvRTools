from os import path
from flask import (render_template,
                   url_for,
                   flash,
                   redirect,
                   send_from_directory)
from rvr_tools.forms import CalcMdfForm, RandomizeForm
from rvr_tools.calculator import MDF
from rvr_tools import app


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    if False:
        return redirect(url_for('home'))
    return render_template('about.html')


@app.route("/randomize", methods=['GET', 'POST'])
def randomize():
    form = RandomizeForm()
    if form.validate_on_submit():
        # range_ = MyRange(form.range_str.data)
        # range_str = randomize_suits_for_range(range_)
        range_str = ''
        flash('successfully randomized', 'success')
        return render_template('randomize.html',
                               titel='Randomize',
                               form=form,
                               r=range_str)
    return render_template('randomize.html', titel='Randomize', form=form)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = CalcMdfForm()
    if form.validate_on_submit():
        pot = form.pot.data
        bet = form.bet.data
        invest = form.invest.data
        v_invest = form.v_invest.data
        mdf = MDF(pot=pot, bet=bet, invest=invest, villain_invest=v_invest)
        flash('Calculated MDF and Alpha', 'success')
        return render_template('calculator.html',
                               titel='Randomize',
                               form=form,
                               mdf=round(mdf.mdf_pct, 1),
                               alpha=round(mdf.alpha_pct, 1))
    return render_template('calculator.html', titel='Randomize', form=form)
