from . import app


@app.route('/')
def inicio():

    return 'Comienza el juego'
