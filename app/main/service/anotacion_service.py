from app.main import db
from app.main.model.anotacion import Anotacion
from app.main.model.valor import Valor
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.model.color import Color
from app.main.model.usuario import Usuario
from app.main.model.parrafo import Parrafo
from app.main.model.politica import Politica, PoliticaUsuarioRelacion
from app.main.model.rol_usuario import RolUsuario
from app.main.util.dto import AnotacionDto
from app.main.service.valor_service import obtener_valor
from app.main.util.clases_auxiliares import AnotacionConsultar, AnotacionConsultarAnotador, \
    ConsultarAnotacionesAnotadoresParrafo, AnotacionesAnotadoresConsultarRespuesta
from flask_restplus import marshal
import datetime

_anotacionesConsultar = AnotacionDto.anotacionConsultar


def consultar_inconsistencia_consolidacion(anotacion_actual, parrafo_id):
    anotaciones_tuplas = []
    anotaciones_tuplas.append(anotacion_actual)
    usuarios = (db.session.query(Parrafo, Politica, PoliticaUsuarioRelacion)
                .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                .outerjoin(PoliticaUsuarioRelacion, Politica.id == PoliticaUsuarioRelacion.politica_id)
                .filter(Parrafo.id == parrafo_id,
                        PoliticaUsuarioRelacion.consolidar == False).all())

    for usuario in usuarios:
        print(usuario[2].usuario_id)
        anotaciones_parrafo = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Parrafo)
                                .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                                .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                                .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                                .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                                .filter(Parrafo.id == parrafo_id,
                                        Anotacion.usuario_id == usuario[2].usuario_id,
                                        Anotacion.consolidar == False).all())
        i = 0
        anotacion_usuario = []
        for anotacion in anotaciones_parrafo:
            tupla = (anotacion[3].id, anotacion[2].id, anotacion[1].id, anotacion[0].permite)
            anotacion_usuario.insert(i, tupla)
            i += 1
        anotaciones_tuplas.append(anotacion_usuario)
        print(anotaciones_tuplas)
    inconsistencia = not all(x == anotaciones_tuplas[0] for x in anotaciones_tuplas)

    return inconsistencia


def consultar_inconsistencia_notificacion(data):
    valor_consulta = obtener_valor(data['valor_id'])

    tupla_anotacion = (valor_consulta[0].get('tratamiento_id'),
                           valor_consulta[0].get('atributo_id'),
                           valor_consulta[0].get('id'),
                           data['permite'])
    print(consultar_inconsistencia_notificacion(tupla_anotacion, data['parrafo_id']))


def guardar_anotacion(data):
    nueva_anotacion= Anotacion(
        fecha_anotado=datetime.datetime.isoformat(datetime.datetime.now()),
        texto=data['texto'],
        texto_html=data['texto_html'],
        comentario=data['comentario'],
        valor_id=data['valor_id'],
        parrafo_id=data['parrafo_id'],
        usuario_id=data['usuario_id'],
        permite=data['permite']
    )
    guardar_cambios(nueva_anotacion)
    respuesta = {
        'estado': 'exito',
        'mensaje': 'Anotacion registrada exitosamente.'
    }
    return respuesta, 201


def editar_anotacion(data):
    anotacion = Anotacion.query.filter_by(id=data['id']).first()
    if not anotacion:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Error editando anotacion'
        }
        return respuesta, 409
    else:
        anotacion.texto = data['texto']
        anotacion.texto_html = data['texto_html']
        anotacion.comentario = data['comentario']
        anotacion.permite = data['permite']
        guardar_cambios(anotacion)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Anotacion editada exitosamente.'
        }
        return respuesta, 201


def eliminar_anotacion(id):
    try:
        db.session.query(Anotacion).filter(Anotacion.id == id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Error eliminando anotacion'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Anotacion eliminada exitosamente.'
        }
        return respuesta, 201


def obtener_anotaciones_parrafo(parrafo_id):
    anotaciones = Anotacion.query.filter_by(parrafo_id=parrafo_id).all()
    return anotaciones


def obtener_total_anotaciones_parrafo_anotador(data):
    anotaciones_anotador_total = db.session.query(Anotacion)\
                                .filter(Anotacion.usuario_id == data['usuario_id'],
                                        Anotacion.parrafo_id == data['parrafo_id'],
                                        Anotacion.consolidar == False).count()
    respuesta = {
        'estado': 'exito',
        'num_anotaciones': anotaciones_anotador_total
    }
    return respuesta, 201


def obtener_anotaciones_parrafo_anotador(data):
    anotaciones_anotador = Anotacion.query.filter_by(usuario_id=data['usuario_id'],
                                                     parrafo_id=data['parrafo_id'],
                                                     consolidar=False).all()
    if not anotaciones_anotador:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existen anotaciones'
        }
        return respuesta, 409

    else:
        return anotaciones_anotador, 201


def obtener_anotaciones_politica_anotadores(politica_id):
    anotaciones = [AnotacionConsultar]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario, Parrafo, Politica)
                             .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                             .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                             .filter(Politica.id == politica_id, Usuario.rol_usuario == 2).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para esta politica'
        }
        return respuesta, 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_id = item[2].id
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_id = item[3].id
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].usuario_nombre = item[4].email
            i += 1
        return marshal(anotaciones, _anotacionesConsultar), 201


def obtener_anotaciones_parrafo_anotador(data):
    anotaciones = [AnotacionConsultarAnotador]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .filter(Anotacion.parrafo_id == data['parrafo_id'],
                                     Anotacion.usuario_id == data['usuario_id'],
                                     Anotacion.consolidar == False).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para este parrafo'
        }
        return respuesta, 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].color_primario = item[3].color_tratamiento.codigo
            i += 1
        return marshal(anotaciones, AnotacionDto.anotacionConsultarAnotadores), 201


def obtener_anotaciones_parrafo_anotadores(parrafo_id):
    anotaciones = [AnotacionConsultar]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                             .filter(Anotacion.parrafo_id == parrafo_id, Anotacion.consolidar ==False).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para este parrafo'
        }
        return respuesta, 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_id = item[2].id
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_id = item[3].id
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].usuario_nombre = item[4].email
            i += 1
        return marshal(anotaciones, AnotacionDto.anotacionConsultar), 201


def obtener_anotaciones_politica_consolidador(parrafo_id):
    anotaciones = [AnotacionConsultar]
    anotaciones_consultar = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario)
                             .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                             .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                             .filter(Anotacion.parrafo_id == parrafo_id, Usuario.rol_usuario == 1).all())
    anotaciones.clear()
    i = 0
    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para esta politica'
        }
        return respuesta, 404
    else:
        for item in anotaciones_consultar:
            anotaciones.insert(i, item[0])
            anotaciones[i].valor_descripcion = item[1].descripcion
            anotaciones[i].atributo_id = item[2].id
            anotaciones[i].atributo_descripcion = item[2].descripcion
            anotaciones[i].tratamiento_id = item[3].id
            anotaciones[i].tratamiento_descripcion = item[3].descripcion
            anotaciones[i].usuario_nombre = item[4].email
            i += 1
        return anotaciones, 201


def consultar_ultima_anotacion_usuario_politica(politica_id, usuario_id, consolidar):
    ultimo_parrafo_anotado = (db.session.query(Anotacion.parrafo_id.distinct(), Parrafo, Politica)
                              .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                              .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                              .filter(Politica.id == politica_id,
                                      Anotacion.usuario_id == usuario_id,
                                      Anotacion.consolidar == consolidar).count())
    return ultimo_parrafo_anotado


def consultar_anotaciones_usuario(politica_id, secuencia, usuario_id):
    anotaciones_usuario = [AnotacionConsultarAnotador]
    anotaciones_parrafo_usuarios = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Usuario, Parrafo, Color)
                                    .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                                    .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                                    .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                                    .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                                    .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                                    .outerjoin(Color, Color.id == Tratamiento.color_primario)
                                    .filter(Parrafo.politica_id == politica_id,
                                            Parrafo.secuencia == secuencia,
                                            Anotacion.usuario_id == usuario_id,
                                            Anotacion.consolidar == False).all())
    anotaciones_usuario.clear()
    i = 0
    if not anotaciones_parrafo_usuarios:
        return []
    else:
        for item in anotaciones_parrafo_usuarios:
            anotaciones_usuario.insert(i, item[0])
            anotaciones_usuario[i].valor_descripcion = item[1].descripcion
            anotaciones_usuario[i].atributo_descripcion = item[2].descripcion
            anotaciones_usuario[i].tratamiento_descripcion = item[3].descripcion
            anotaciones_usuario[i].color_primario = item[6].codigo
            i += 1
        return anotaciones_usuario


def consultar_inconsistencia_anotador(politica_id, secuencia, usuarios):
    anotaciones_tuplas = []
    for usuario in usuarios:
        anotaciones_parrafo = (db.session.query(Anotacion, Valor, Atributo, Tratamiento, Parrafo)
                                .outerjoin(Valor, Anotacion.valor_id == Valor.id)
                                .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                                .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                                .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                                .filter(Parrafo.politica_id == politica_id,
                                        Parrafo.secuencia == secuencia,
                                        Anotacion.usuario_id == usuario[1].id,
                                        Anotacion.consolidar == False).all())
        i = 0
        anotacion_usuario = []
        for anotacion in anotaciones_parrafo:
            tupla = (anotacion[3].id, anotacion[2].id, anotacion[1].id)
            anotacion_usuario.insert(i, tupla)
            i += 1
        anotaciones_tuplas.append(anotacion_usuario)

    inconsistencia = not all(x == anotaciones_tuplas[0] for x in anotaciones_tuplas)

    return inconsistencia


def consultar_anotaciones_usuarios_anotadores(politica_id, secuencia):
    db.session.configure(autoflush=False)
    usuarios_anotaciones = AnotacionesAnotadoresConsultarRespuesta
    anotaciones = [ConsultarAnotacionesAnotadoresParrafo]
    anotaciones_aux = []
    usuarios = (db.session.query(PoliticaUsuarioRelacion, Usuario, RolUsuario)
                .outerjoin(Usuario, PoliticaUsuarioRelacion.usuario_id == Usuario.id)
                .outerjoin(RolUsuario, Usuario.rol_usuario == RolUsuario.id)
                .filter(PoliticaUsuarioRelacion.politica_id == politica_id,
                        PoliticaUsuarioRelacion.consolidar == False).all())

    i = 0
    anotaciones.clear()
    for usuario in usuarios:
        anotaciones.insert(i, usuario[1])
        anotaciones[i].rol_usuario = usuario[2].nombre
        anotaciones_aux.clear()
        anotaciones_aux = consultar_anotaciones_usuario(politica_id, secuencia, usuario[1].id)
        anotaciones[i].anotaciones = anotaciones_aux

    usuarios_anotaciones.inconsistencia = consultar_inconsistencia_anotador(politica_id,secuencia, usuarios)
    usuarios_anotaciones.usuarios_anotaciones = anotaciones

    return marshal(usuarios_anotaciones, AnotacionDto.anotacionesAnotadoresConsultarRespuesta), 201


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()