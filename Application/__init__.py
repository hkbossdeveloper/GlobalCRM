from flask import Flask
app = Flask(__name__)
app.config.from_object('config.ProductionConfig')


from Application.views.Master import login , dashboard , employee