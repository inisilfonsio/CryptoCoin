from flask import jsonify, render_template, request, session
from flask_login import current_user

from . import app
from balance.models import *
from config import RUTA_PORTFOLIO


@app.route('/inicio')
def inicio():
    if 'nombre_usuario' in session:
        nombre_usuario = session['nombre_usuario']

    return render_template('index.html', user=current_user,
                           nombre_usuario=nombre_usuario)


@app.route('/comprar')
def compra():

    return 'Aqui se compra criptos'


@app.route('/status', methods=['GET', 'POST'])
def estado():
    return 'Aquí se comprueba la inversion'
