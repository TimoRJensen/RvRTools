from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextAreaField, TextField
from wtforms.validators import DataRequired, Length, NumberRange


class RandomizeForm(FlaskForm):
    range_str = TextAreaField('Range Input',
                              validators=[DataRequired()],
                              default='AA-JJ, [25]ATs+, AQo+[/25]')
    submit = SubmitField('Randomize')


class CalcMdfForm(FlaskForm):
    pot = IntegerField('Pot size',
                       validators=[NumberRange(min=0, max=1000)],
                       render_kw={'readonly': True},
                       )
    bet = IntegerField('Bet',
                       validators=[NumberRange(min=2, max=200),
                                   DataRequired()],
                       render_kw={'readonly': True},
                       )
    invest = IntegerField('Your previous invest',
                          validators=[NumberRange(min=0,
                                                  max=200
                                                  )
                                      ],
                          default=0,
                          render_kw={'readonly': True},
                          )
    v_invest = IntegerField("Villain's previous invest",
                            validators=[NumberRange(min=0,
                                                    max=200
                                                    )
                                        ],
                            default=0,
                            render_kw={'readonly': True},
                            )
    formula = TextAreaField('Formula',
                            render_kw={'readonly': True}
                            )
    # submit = SubmitField('Calculate')  # let's see if we can make this work
    # without a submit per section


class GetGameForm(FlaskForm):
    game_id = TextField('Game ID', validators=[DataRequired(),
                                               Length(min=4, max=5)])
    submit = SubmitField('Get Game')


class BetSizeForm(FlaskForm):
    pot = IntegerField('Pot size', validators=[NumberRange(min=0, max=1000)],
                       render_kw={'readonly': True},
                       )
    bet = IntegerField('Bet', validators=[NumberRange(min=2, max=200),
                                          DataRequired()],
                       render_kw={'readonly': True},
                       )
