from app.main import db
from app.main.model.politica import Politica, PoliticaUsuarioRelacion
from app.main.model.parrafo import Parrafo
from flask import request
from flask_restplus import marshal
from werkzeug.utils import secure_filename
from ..util.clases_auxiliares import PoliticaMostrar, ParrafoMostrar, ParrafoGuardar, PoliticaAnotadorNoFinalizadas, \
    PoliticaConsultarParrafos
from ..util.dto import PoliticaDto
from ..service.parrafo_service import guardar_parrafo, consultar_num_parrafos_politica
from ..service.anotacion_service import consultar_ultima_anotacion_usuario_politica
import os

EXTENSIONES_PERMITIDAS = {'txt'}

if os.name == 'nt':
    CARPETA_SUBIDA = os.getcwd() + '\Politicas\\'
else:
    CARPETA_SUBIDA = os.getcwd() + '/Politicas/'

politica_respuesta = PoliticaMostrar
politica_respuesta.parrafos = []


def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and\
           nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS


def politica_existe_peticion():
    if 'politica' not in request.files:
        return False
    else:
        return True


def abrir_politica(nombre_archivo):
    with open(CARPETA_SUBIDA + nombre_archivo, 'r') as txt:
        politica = txt.read()
        return politica


def existe_archivo_politica_mismo_nombre(nombre_archivo):
    try:
        with open(CARPETA_SUBIDA + nombre_archivo, 'r') as txt:
            return True
    except:
        return False


def separar_parrafos_principales(politica):
    parrafos = politica.split('\n\n\n')
    return parrafos


def separar_parrafos_secundarios(parrafo):
    subparrafos = parrafo.split('\n')
    return subparrafos


def llenar_politica_mostrar():
    peticion = request.form.to_dict()
    politica_respuesta.nombre = peticion.get('nombre')
    politica_respuesta.fecha = peticion.get('fecha')
    politica_respuesta.url = peticion.get('url')
    politica_respuesta.parrafos = []


def borrar_politica_previsualizacion(archivo):
    try:
        os.remove(CARPETA_SUBIDA + archivo.filename)
    except:
        respuesta = {
            'estado': 'fallido',
            'mesaje': 'Existe un problema con la eliminacion del archivo en el servidor'
        }
        return respuesta, 409


def error_directorio():
    try:
        os.mkdir(CARPETA_SUBIDA)
    except OSError:
        return False
    else:
        return True


def llenar_politica_html(parrafos):
    politica_respuesta.parrafos.clear()
    i = 0
    for parrafo in parrafos:
        texto = ''
        texto_html = ''
        titulo = ''

        subparrafos = separar_parrafos_secundarios(parrafo)

        if subparrafos[0].startswith("+", 0, 1):
            # retiramos el caracter '+'
            titulo += subparrafos[0][1:]
            subparrafos.remove(subparrafos[0])

        for subparrafo in subparrafos:
            if subparrafo != '':
                texto += subparrafo + ' '
                texto_html += subparrafo + '<br><br>'

        parrafo_aux = ParrafoMostrar(titulo, texto, texto_html)
        politica_respuesta.parrafos.insert(i, parrafo_aux)
        i += 1

    return politica_respuesta


def previsualizar_politica():
    if not politica_existe_peticion():
        respuesta = {
            'estado': 'fallido',
            'mesaje': 'No existe el archivo en la peticion'
        }
        return respuesta, 409

    archivo = request.files['politica']

    if not archivo_permitido(archivo.filename):
        respuesta = {
            'estado': 'fallido',
            'mesaje': 'Extension de archivo invalida'
        }
        return respuesta, 409

    if existe_archivo_politica_mismo_nombre(archivo.filename):
        respuesta = {
            'estado': 'fallido',
            'mesaje': 'Ya existe un archivo con ese nombre'
        }
        return respuesta, 409

    if archivo:
        if os.path.isdir(CARPETA_SUBIDA):
            archivo.filename = archivo.filename.strip().replace(" ", "")
            nombre_archivo = secure_filename(archivo.filename)

            try:
                archivo.save(os.path.join(CARPETA_SUBIDA, nombre_archivo))
            except:
                respuesta = {
                    'estado': 'fallido',
                    'mesaje': 'Existe un problema con la creacion del archivo en el servidor'
                }
                return respuesta, 409

            politica = abrir_politica(nombre_archivo)
            parrafos = separar_parrafos_principales(politica)
            llenar_politica_mostrar()
            json = llenar_politica_html(parrafos)
            borrar_politica_previsualizacion(archivo)

            respuesta = {
                'estado': 'exito',
                'mensaje': 'politica creada',
                'politica': marshal(json, PoliticaDto.politicaMostrar)
            }

            return respuesta, 201
        else:
            os.mkdir(CARPETA_SUBIDA)

            archivo.filename = archivo.filename.strip().replace(" ", "")
            nombre_archivo = secure_filename(archivo.filename)

            try:
                archivo.save(os.path.join(CARPETA_SUBIDA, nombre_archivo))
            except:
                respuesta = {
                    'estado': 'fallido',
                    'mesaje': 'Existe un problema con la creacion del archivo en el servidor'
                }
                return respuesta, 409

            politica = abrir_politica(nombre_archivo)
            parrafos = separar_parrafos_principales(politica)
            llenar_politica_mostrar()
            json = llenar_politica_html(parrafos)
            borrar_politica_previsualizacion(archivo)

            respuesta = {
                'estado': 'exito',
                'mensaje': 'politica creada',
                'politica': marshal(json, PoliticaDto.politicaMostrar)
            }

            return respuesta, 201
    else:
        error_directorio()


def guardar_politica():
    respuesta = request.form.to_dict()
    politica = Politica.query.filter_by(nombre=respuesta.get('nombre')).first()
    if not politica:
            fecha_aux = respuesta.get('fecha').split('T')[0]
            nueva_politica = Politica(
                nombre=respuesta.get('nombre'),
                url=respuesta.get('url'),
                fecha=fecha_aux,
                asignada=False
            )

            guardar_cambios(nueva_politica)


            #GUARDAR PARRAFOS
            archivo = request.files['politica']

            if archivo:
                if os.path.isdir(CARPETA_SUBIDA):

                    if existe_archivo_politica_mismo_nombre(archivo.filename):
                        respuesta = {
                            'estado': 'fallido',
                            'mesaje': 'Existe un archivo con el mismo nombre'
                        }
                        return respuesta, 409

                    archivo.filename = archivo.filename.strip().replace(" ", "")
                    nombre_archivo = secure_filename(archivo.filename)

                    try:
                        archivo.save(os.path.join(CARPETA_SUBIDA, nombre_archivo))
                    except:
                        respuesta = {
                            'estado': 'fallido',
                            'mesaje': 'Existe un problema con la creacion del archivo en el servidor'
                        }
                        return respuesta, 409

                    politica = abrir_politica(nombre_archivo)
                    parrafos = separar_parrafos_principales(politica)
                    politica_procesada = llenar_politica_html(parrafos)

                    i = 0
                    for parrafo in politica_procesada.parrafos:
                        parrafo_aux = ParrafoGuardar(i, parrafo.titulo, parrafo.texto, parrafo.texto_html,
                                                     nueva_politica.id)
                        guardar_parrafo(parrafo_aux)
                        i += 1

                    borrar_politica_previsualizacion(archivo)
                    respuesta = {
                        'estado': 'exito',
                        'mesaje': 'Politica cargada con exito'
                    }
                    return respuesta, 201

    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'El nombre de la politica ya existe'
        }
        return respuesta, 409


def editar_politica(data):
    politica = Politica.query.filter_by(id=data['id']).first()
    if not politica:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe politica de privacidad'
        }
        return respuesta, 409
    else:
        fecha_aux = data['fecha'].split('T')[0]
        politica.nombre = data['nombre']
        politica.url = data['url']
        politica.fecha = fecha_aux

        try:
            guardar_cambios(politica)
        except:
            respuesta = {
                'estado': 'fallido',
                'mensaje': 'Error editando politica'
            }
            return respuesta, 409
        else:
            respuesta = {
                'estado': 'exito',
                'mensaje': 'Politca edita con exita'
            }
            return respuesta, 201


def eliminar_politica(id):
    try:
        Parrafo.query.filter_by(politica_id=id).delete()
        Politica.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Error eliminando politica'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Politica eliminada con exito'
        }
        return respuesta, 201


def actualizar_politica_asignada(data):
    politica_aux = Politica.query.filter_by(id=data['id']).first()
    if not politica_aux:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Error actualizando politica asignada'
        }
        return respuesta, 409
    else:
        politica_aux.asignada = True
        guardar_cambios(politica_aux)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Politica asignada actualizado con exito'
        }
        return respuesta, 201


def consultar_politicas():
    politicas = Politica.query.all()
    return marshal(politicas, PoliticaDto.politicaConsultar), 201


def consultar_politica_parrafos(politica_id):
    politica_parrafos = PoliticaConsultarParrafos
    politica_parrafos.parrafos = []
    parrafos_consulta = (db.session.query(Politica).filter(Politica.id == politica_id).all())

    if not parrafos_consulta:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe la politica'
        }
        return respuesta, 409
    else:
        politica_parrafos.nombre = parrafos_consulta[0].nombre
        for parrafo in parrafos_consulta[0].parrafos:
            politica_parrafos.parrafos.append(parrafo)
        return marshal(politica_parrafos, PoliticaDto.politicaConsultarParrafos), 201


def consultar_politicas_consolidador_no_finalizadas(consolidador_id):
    politicas_anotar = [PoliticaAnotadorNoFinalizadas]
    politicas_anotar_sql = (db.session.query(PoliticaUsuarioRelacion, Politica)
                            .outerjoin(Politica, PoliticaUsuarioRelacion.politica_id == Politica.id)
                            .filter(PoliticaUsuarioRelacion.usuario_id == consolidador_id,
                                    PoliticaUsuarioRelacion.consolidar == True,
                                    PoliticaUsuarioRelacion.finalizado == False).all())

    if not politicas_anotar_sql:
        respuesta = {
            "estado": "fallido",
            "mensaje": "El usuario no tiene politicas por consolidar"
        }
        return respuesta, 409
    else:
        i = 0
        politicas_anotar.clear()
        for item in politicas_anotar_sql:
            if politica_lista_para_consolidar(item[0].politica_id):
                politicas_anotar.insert(i, item[0])
                politicas_anotar[i].politica_nombre = item[1].nombre
                politicas_anotar[i].progreso = calcular_progeso_politica(politicas_anotar[i].politica_id, consolidador_id,True)
                i += 1

        return marshal(politicas_anotar, PoliticaDto.politicaAnotarNoFinalizada), 201


def consultar_politicas_anotador_no_finalizadas(usuario_id):
    politicas_anotar = [PoliticaAnotadorNoFinalizadas]
    politicas_anotar_sql = (db.session.query(PoliticaUsuarioRelacion, Politica)
                            .outerjoin(Politica, PoliticaUsuarioRelacion.politica_id == Politica.id)
                            .filter(PoliticaUsuarioRelacion.usuario_id == usuario_id,
                                    PoliticaUsuarioRelacion.consolidar == False,
                                    PoliticaUsuarioRelacion.finalizado == False).all())

    if not politicas_anotar_sql:
        respuesta = {
            "estado": "fallido",
            "mensaje": "El usuario no tiene politicas por anotar"
        }
        return respuesta, 409
    else:
        i = 0
        politicas_anotar.clear()
        for item in politicas_anotar_sql:
            politicas_anotar.insert(i, item[0])
            politicas_anotar[i].politica_nombre = item[1].nombre
            politicas_anotar[i].progreso = calcular_progeso_politica(politicas_anotar[i].politica_id, usuario_id, False)
            i += 1
        return marshal(politicas_anotar, PoliticaDto.politicaAnotarNoFinalizada), 201


def calcular_progeso_politica(politica_id, usuario_id, consolidar):
    num_parrafos = consultar_num_parrafos_politica(politica_id)
    ultimo_parrafo_anotado = consultar_ultima_anotacion_usuario_politica(politica_id, usuario_id, consolidar)
    return (ultimo_parrafo_anotado/num_parrafos) * 100


def guardar_usuario_politica(data):
    politica_usuario = PoliticaUsuarioRelacion.query.filter_by(
        politica_id=data['politica_id'],
        usuario_id=data['usuario_id'],
        consolidar=data["consolidar"]).first()
    if not politica_usuario:
        nueva_politica_usuario = PoliticaUsuarioRelacion(
            politica_id=data['politica_id'],
            usuario_id=data['usuario_id'],
            consolidar=data['consolidar'],
            finalizado=False
        )
        guardar_cambios(nueva_politica_usuario)
        respuesta = {
            'estado': 'exito',
            'mesaje': 'Usuario asignado exitosamente'
        }
        return respuesta, 201
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Politica ya asignada'
        }
        return respuesta, 409


def actualizar_anotador_politica(data):
    politica_usuario = PoliticaUsuarioRelacion.query.filter_by(politica_id=data['politica_id'],
                                                               usuario_id=data['usuario_id'],
                                                               consolidar=False).first()

    if politica_usuario:
        politica_usuario.finalizado = True
        guardar_cambios(politica_usuario)
        respuesta = {
            "estado": "exito",
            "mensaje": "Politica usuario actualizada exitosamente"
        }
        return respuesta, 201
    else:
        respuesta = {
            "estado": "fallido",
            "mensaje": "Politica usuario no encontrada"
        }
        return respuesta, 409


def politica_lista_para_consolidar(politica_id):
    politica_anotadores_consulta = (db.session.query(PoliticaUsuarioRelacion)
                                    .filter(PoliticaUsuarioRelacion.politica_id == politica_id,
                                            PoliticaUsuarioRelacion.consolidar == False).all())
    if not politica_anotadores_consulta:
        return "NO"
    else:
        listo = False
        for anotador in politica_anotadores_consulta:
            if anotador.finalizado:
                listo = True
            else:
                listo = False
        return listo


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()





