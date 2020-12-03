from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextAreaField, TextField
from wtforms.validators import DataRequired, Length, NumberRange


class RandomizeForm(FlaskForm):
    range_str = TextAreaField('Range Input',
                              validators=[DataRequired()],
                              default='AA-JJ, [25]ATs+, AQo+[/25]')
    submit = SubmitField('Randomize')


class CalcMdfForm(FlaskForm):
    pot = IntegerField('Pot size', validators=[NumberRange(min=5, max=1000),
                                               DataRequired()])
    bet = IntegerField('Bet', validators=[NumberRange(min=2, max=200),
                                          DataRequired()])
    invest = IntegerField('Your previous invest',
                          validators=[NumberRange(min=0,
                                                  max=200
                                                  )
                                      ],
                          default=0
                          )
    v_invest = IntegerField("Villain's previous invest",
                            validators=[NumberRange(min=0,
                                                    max=200
                                                    )
                                        ],
                            default=0
                            )
    submit = SubmitField('Calculate')


class GetGameForm(FlaskForm):
    game_id = TextField('Game ID', validators=[DataRequired(),
                                               Length(min=4, max=5)])
    submit = SubmitField('Get Game')
