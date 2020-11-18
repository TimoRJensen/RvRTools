from flask import render_template, url_for, flash, redirect
from rvr_tools.forms import RandomizeForm
from rvr_tools import app


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

@app.route('/calculator')
def calculator():
    return render_template('calculator.html', titel='Randomize')
