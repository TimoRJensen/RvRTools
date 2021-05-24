from os import path
from flask import (render_template,
                   #    url_for,
                   #    flash,
                   #    redirect,
                   send_from_directory)
from rvr_tools.forms import (BetSizeForm,
                             CalcMdfForm,
                             GetGameForm,
                             RandomizeForm)
from rvr_tools.calculator import MDF
from rvr_tools import app
from pynlh import Range
from .game_scraper import Game


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/randomize", methods=['GET', 'POST'])
def randomize():
    form = RandomizeForm()
    if form.validate_on_submit():
        range_ = Range(form.range_str.data)
        # range_str = range_.randomize_suits_for_range()  # old randomizer
        range_str = range_.apply_rng().to_str(remove_freq_tags=True)
        # flash('successfully randomized', 'success')
        return render_template('randomize.html',
                               titel='Randomizer',
                               form=form,
                               r=range_str)
    return render_template('randomize.html', titel='Randomize', form=form)


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    mdf_form = CalcMdfForm()
    get_form = GetGameForm()
    size_form = BetSizeForm()
    if get_form.validate_on_submit():
        game_id = get_form.game_id.data
        try:
            scraper = Game(game_id)
            pot = scraper.pot
            invest = scraper.hero.invest
            mdf_form.pot.data = pot
            mdf_form.invest.data = invest
            if scraper.history.last_street == 'Preflop':
                bet = (scraper.last_bet - scraper.acted_last.init_invest)
                mdf_form.bet.data = bet
                v_invest = scraper.acted_last.init_invest
            else:
                bet = scraper.last_bet
                mdf_form.bet.data = bet
                v_invest = scraper.acted_last.invest
            mdf_form.v_invest.data = v_invest
            mdf_form.formula.data = (f"MDF = 1 - ({bet} / ({pot} + {invest} + "
                                     f"{v_invest} + {bet}))")
            mdf = MDF(pot=scraper.pot,
                      bet=bet,
                      invest=invest,
                      villain_invest=v_invest,
                      )
            get_form.game_id.data = game_id
            size_form.pot.data = pot
            size_form.bet.data = bet
            third = scraper.next_bet(.33)
            half = scraper.next_bet(.5)
            threeq = scraper.next_bet(.75)
            psb = scraper.next_bet(1)
        except TypeError:  # noqa: E722
            get_form.game_id.errors = ("""Sorry can't handle this game state
                                          yet.""",)
            return render_template('calculator.html',
                                   titel='Calculator',
                                   mdf_form=mdf_form,
                                   get_form=get_form,
                                   size_form=size_form,)
        return render_template('calculator.html',
                               titel='Calculator',
                               mdf_form=mdf_form,
                               mdf=round(mdf.mdf_pct, 1),
                               get_form=get_form,
                               alpha=round(mdf.alpha_pct, 1),
                               size_form=size_form,
                               third=third,
                               half=half,
                               threeq=threeq,
                               psb=psb,
                               scraper=scraper,
                               )
    return render_template('calculator.html',
                           titel='Calculator',
                           mdf_form=mdf_form,
                           get_form=get_form,
                           size_form=size_form,
                           scraper=None,
                           mdf=0,
                           alpha=0,
                           third=0,
                           half=0,
                           threeq=0,
                           psb=0,
                           )
