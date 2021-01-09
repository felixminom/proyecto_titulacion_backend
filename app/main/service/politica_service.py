from app.main import db
from app.main.model.politica import Politica, PoliticaUsuarioRelacion
from app.main.model.usuario import Usuario
from flask import request
from flask_restplus import marshal
from werkzeug.utils import secure_filename
from ..util.clases_auxiliares import PoliticaMostrar, ParrafoMostrar, ParrafoGuardar, PoliticaAnotadorNoFinalizadas, \
    PoliticaConsultarParrafos
from ..util.dto import PoliticaDto
from ..service.parrafo_service import guardar_parrafo, consultar_num_parrafos_politica, eliminar_parrafos_politica
from ..service.anotacion_service import consultar_ultima_anotacion_usuario_politica, calcular_coeficiente_interanotador
import os

EXTENSIONES_PERMITIDAS = {'txt'}

#verificamos sistema operativo
#esto se hizo ya que el desarrollo se realizo en un sistema operativo windows
#y el sistema se encuentra alojada en un servidor ubuntu
if os.name == 'nt':
    CARPETA_SUBIDA = os.getcwd() + '\Politicas\\'
else:
    CARPETA_SUBIDA = os.getcwd() + '/Politicas/'

politica_respuesta = PoliticaMostrar
politica_respuesta.parrafos = []

#Se limita las extensiones de archivo que se va a guardar
def archivo_permitido(nombre_archivo):
    return '.' in nombre_archivo and \
           nombre_archivo.rsplit('.', 1)[1].lower() in EXTENSIONES_PERMITIDAS


#Se verifica si un archivo existe en la petición enviada desde el frontend
def politica_existe_peticion():
    if 'politica' not in request.files:
        return False
    else:
        return True

#luego de guardar la política se lee su archivo
def abrir_politica(nombre_archivo):
    with open(CARPETA_SUBIDA + nombre_archivo, 'r') as txt:
        politica = txt.read()
        return politica

#Verifica que no existan politicas con nombre duplicado
def existe_archivo_politica_mismo_nombre(nombre_archivo):
    try:
        with open(CARPETA_SUBIDA + nombre_archivo, 'r') as txt:
            return True
    except:
        return False

#Separa los parrafos de una política de privacidad
def separar_parrafos_principales(politica):
    parrafos = politica.split('\n\n\n')
    return parrafos

#Separa un parrafo en cada salto de linea
def separar_parrafos_secundarios(parrafo):
    subparrafos = parrafo.split('\n')
    return subparrafos

#Llenamos los datos para previsualizar
def llenar_politica_mostrar():
    peticion = request.form.to_dict()
    politica_respuesta.nombre = peticion.get('nombre')
    politica_respuesta.fecha = peticion.get('fecha')
    politica_respuesta.url = peticion.get('url')
    politica_respuesta.parrafos = []

#Se borra el archivo de la politica una vez previsualizad
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
            #remplazamos saltos de linea por espacios en blanco o por saltos de linea html (<br>)
            if subparrafo != '':
                texto += subparrafo + ' '
                texto_html += subparrafo + '<br><br>'

        parrafo_aux = ParrafoMostrar(titulo, texto, texto_html)
        politica_respuesta.parrafos.insert(i, parrafo_aux)
        i += 1

    return politica_respuesta


#Función previsualizacion de política
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

        # GUARDAR PARRAFOS
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
        eliminar_parrafos_politica(politica_id=id)
        Politica.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Error eliminando política'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Política eliminada con exito'
        }
        return respuesta, 201


def actualizar_politica_asignada(data):
    """ Actualiza el campo 'asignada' de una política """
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

#Consulta todas las políticas de privacidad
def consultar_politicas():
    politicas = Politica.query.all()
    return marshal(politicas, PoliticaDto.politicaConsultar), 201

#Consulta parrafos de una política
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
    """ Consulta las políticas de un consolidador que aún no han sido finalizadas"""
    politicas_anotar = []
    politicas_anotar_consulta = (db.session.query(PoliticaUsuarioRelacion, Politica)
                                 .outerjoin(Politica, PoliticaUsuarioRelacion.politica_id == Politica.id)
                                 .filter(PoliticaUsuarioRelacion.usuario_id == consolidador_id,
                                         PoliticaUsuarioRelacion.consolidar == True,
                                         PoliticaUsuarioRelacion.finalizado == False, ).all())

    if not politicas_anotar_consulta:
        return [], 201
    else:
        i = 0
        for item in politicas_anotar_consulta:
            if politica_lista_para_consolidar(item[0].politica_id):
                politicas_anotar.insert(i, item[0])
                politicas_anotar[i].politica_nombre = item[1].nombre
                politicas_anotar[i].progreso = calcular_progeso_politica(politicas_anotar[i].politica_id,
                                                                         consolidador_id,
                                                                         True)
                i += 1

        return marshal(politicas_anotar, PoliticaDto.politicaAnotarNoFinalizada), 201


def consultar_politicas_anotador_no_finalizadas(usuario_id):
    """ Consulta las políticas de un anotador que aún no han sido finalizadas"""
    politicas_anotar = [PoliticaAnotadorNoFinalizadas]
    politicas_anotar_sql = (db.session.query(PoliticaUsuarioRelacion, Politica)
                            .outerjoin(Politica, PoliticaUsuarioRelacion.politica_id == Politica.id)
                            .filter(PoliticaUsuarioRelacion.usuario_id == usuario_id,
                                    PoliticaUsuarioRelacion.consolidar == False,
                                    PoliticaUsuarioRelacion.finalizado == False).all())

    if not politicas_anotar_sql:
        return [], 201
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
    """ Calcula el nivel de progreso en la anotacion o consolidación de una política"""
    num_parrafos = consultar_num_parrafos_politica(politica_id)
    ultimo_parrafo_anotado = consultar_ultima_anotacion_usuario_politica(politica_id, usuario_id, consolidar) + 1
    return round((ultimo_parrafo_anotado / num_parrafos) * 100, 2)


def guardar_usuario_politica(data):
    """ Permite asignar una política para consolidar o anotar"""
    politica_usuario = PoliticaUsuarioRelacion.query.filter_by(politica_id=data['politica_id'],
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


def actualizar_usuario_politica_asignada(data):
    """ Marca una política de privacidad como terminada ya sea en anotación o consolidación"""
    politica_usuario = PoliticaUsuarioRelacion.query.filter_by(politica_id=data['politica_id'],
                                                               usuario_id=data['usuario_id'],
                                                               consolidar=data['consolidar']).first()

    if not politica_usuario:
        respuesta = {
            "estado": "fallido",
            "mensaje": "Politica usuario no encontrada"
        }
        return respuesta, 409
    else:
        politica_usuario.finalizado = True
        guardar_cambios(politica_usuario)

        #Se comprueba si una política está lista para consolidar (todos los usuarion terminaron anotacion)
        #Y que no se este modificando en la etapa de consolidación,
        #de ser asi se calcula el coeficiente inter-anotador
        if politica_lista_para_consolidar(data['politica_id']) and data['consolidar'] == False:
            usuarios = (db.session.query(PoliticaUsuarioRelacion, Usuario)
                        .outerjoin(Usuario, PoliticaUsuarioRelacion.usuario_id == Usuario.id)
                        .filter(PoliticaUsuarioRelacion.politica_id == data['politica_id'],
                                PoliticaUsuarioRelacion.consolidar == False).all())

            politica = Politica.query.filter_by(id=data['politica_id']).first()

            politica.coeficiente = round(calcular_coeficiente_interanotador(data['politica_id'], usuarios).item(), 2)

            guardar_cambios(politica)

            respuesta = {
                "estado": "exito",
                "mensaje": "Politica usuario actualizada exitosamente y coeficiente calculado"
            }
            return respuesta, 201

        respuesta = {
            "estado": "exito",
            "mensaje": "Politica usuario actualizada exitosamente"
        }
        return respuesta, 201


def politica_lista_para_consolidar(politica_id):
    """ Se comprueba si una política está lista para consolidar (todos los usuarion terminaron anotacion) """
    politica_anotadores_consulta = (db.session.query(PoliticaUsuarioRelacion)
                                    .filter(PoliticaUsuarioRelacion.politica_id == politica_id,
                                            PoliticaUsuarioRelacion.consolidar == False).all())

    if not politica_anotadores_consulta:
        return False
    else:
        if all(x.finalizado for x in politica_anotadores_consulta):
            return True
        else:
            return False


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
