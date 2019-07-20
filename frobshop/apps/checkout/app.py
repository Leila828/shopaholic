from oscar.apps.checkout import app
from cashondelivery.app import application as cod_app

app.application = cod_app
