from flask import jsonify, redirect, render_template, request, session, url_for

from . import app
from balance.models import *
from config import *


@app.route('/api/v1/movimientos')
def obtener_movimientos():
    try:
        try:
            page = int(request.args.get('p', DEFAULT_PAG))
        except:
            page = DEFAULT_PAG

        try:
            per_page = int(request.args.get('r', PAG_SIZE))
        except:
            per_page = PAG_SIZE

        nombre_usuario = session['nombre_usuario']
        gestor = DBManager(RUTA_PORTFOLIO)
        consulta = f'SELECT {CAMPOS_TABLA} FROM "{nombre_usuario}"'
        movimientos = gestor.consultaSQL(
            consulta, page, per_page)

        consultaTotal = f'SELECT COUNT(*) FROM "{nombre_usuario}"'
        movTotal = gestor.consultaSQL(consultaTotal)
        total = movTotal[0].get('COUNT(*)')

        if len(movimientos) > 0:
            resultado = {
                'status': 'success',
                'results': movimientos,
                'page': page,
                'perPage': per_page,
                'total': total
            }
            # TODO Conseguir que page y perPage dependan del Backend y no de JS
            status_code = 200
        else:
            resultado = {
                'status': 'error',
                'message': f'No hay movimientos en el sistema'
            }
            status_code = 404

    except Exception as error:
        resultado = {
            "status": "error",
            "message": str(error)
        }
        status_code = 500

    return jsonify(resultado), status_code
