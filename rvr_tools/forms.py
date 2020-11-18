from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class RandomizeForm(FlaskForm):
    range_str = StringField('Range Input', validators=[DataRequired()])
    submit = SubmitField('Randomize')


class CalcMDF(FlaskForm):
    pot = IntegerField('Pot size', validators=NumberRange(min=5, max=1000))
    prev_bet = IntegerField('Your previous bet',
                            validators=NumberRange(min=2,
                                                   max=200,
                                                   )
                            )
    bet = IntegerField('Bet',
                       validators=NumberRange(min=2,
                                              max=200,
                                              )
                       )
    submit = SubmitField('Calculate')
