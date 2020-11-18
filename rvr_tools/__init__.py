from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a3c3ef7fa452decefe231a6284f16049'


from rvr_tools import routes  # noqa: F401,E402
