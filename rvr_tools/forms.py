from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class RandomizeForm(FlaskForm):
    range_str = StringField('Range Input', validators=[DataRequired()])
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
