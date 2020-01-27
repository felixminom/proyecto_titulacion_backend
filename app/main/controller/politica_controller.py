from flask import request, flash
from flask_restplus import Resource, reqparse
from werkzeug.utils import secure_filename


from ..util.dto import PoliticaDto

import os

api = PoliticaDto.api

CARPETA_SUBIDA = os.getcwd() + '\Politicas\\'
EXTENSIONES_PERMITIDAS = {'txt'}


def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and\
           nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS


@api.route('/')
class Politica(Resource):
    @api.response(201, 'Poltica procesada y creada')
    @api.doc('Crear nueva politica de privacidad')
    def post(self):
        """Crear nueva politica"""
        if 'politica' not in request.files:
            respuesta = {
                'estado': 'fallido',
                'mesaje': 'no se ha enviado un archivo'
            }

            return respuesta, 409

        archivo = request.files['politica']

        if archivo.filename == '':
            respuesta = {
                'estado': 'fallido',
                'mesaje': 'no se selecciono archivo'
            }
            return respuesta, 409

        if archivo and archivo_permitido(archivo.filename):

            if os.path.isdir(CARPETA_SUBIDA):

                nombre_archivo = secure_filename(archivo.filename)
                archivo.save(os.path.join(CARPETA_SUBIDA, nombre_archivo))

                with open(CARPETA_SUBIDA + nombre_archivo, 'r') as txt:
                    politica = txt.read()

                    parrafos = politica.split('\n\n\n')

                    i = 1

                    for parrafo in parrafos:
                        titulo = '';
                        parrafoFinal = ''
                        s = 1
                        subparrafos = parrafo.split('\n')
                        if subparrafos[0].startswith("+", 0, 1):
                            #retiramos el caracter ''+''
                            titulo += subparrafos[0][1:]
                            subparrafos.remove(subparrafos[0])
                        for subparrafo in subparrafos:
                            if subparrafo != '':
                                    if subparrafos.index(subparrafo) == len(subparrafos)-1:
                                        parrafoFinal += subparrafo
                                    else:
                                        subparrafo = subparrafo + '<br><br>'
                                        s += 1
                                        parrafoFinal  = parrafoFinal + subparrafo

                        if parrafoFinal != '':
                            print('titulo: {}'.format(titulo))
                            print('parrafo: {}'.format(parrafoFinal))
                        else:
                            print('Existe un parrafo vacio')
                        i += 1


                respuesta = {
                    'estado': 'exito',
                    'mensaje': 'politica creada',
                }

                return respuesta, 201

            else:
                try:
                    os.mkdir(CARPETA_SUBIDA)
                except OSError:
                    respuesta = {
                        'estado': 'fallido',
                        'mensaje': 'error creando directorio',
                        'error': OSError.strerror
                    }
                    return respuesta, 409
                else:
                    respuesta = {
                        'estado': 'exito',
                        'mensaje': 'carpeta creada',
                        'error': OSError.strerror
                    }
                    return respuesta, 201


