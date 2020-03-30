from app.main import db
from app.main.model.anotacion import Anotacion, AnotacionValorRelacion
from app.main.model.valor import Valor
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.model.usuario import Usuario
from app.main.model.parrafo import Parrafo
from app.main.model.politica import Politica, PoliticaUsuarioRelacion
from app.main.model.rol_usuario import RolUsuario
from app.main.util.dto import AnotacionDto
from app.main.util.clases_auxiliares import  AnotacionConsultarAnotador, ConsultarAnotacionesAnotadoresParrafo, \
    AnotacionesAnotadoresConsultarRespuesta, AnotacionValor, AnotacionNotificacionConsultar
from flask_restplus import marshal
import datetime

_anotacionesConsultar = AnotacionDto.anotacionConsultar


def guardar_anotacion(data):
    nueva_anotacion= Anotacion(
        fecha_anotado=datetime.datetime.isoformat(datetime.datetime.now()),
        texto=data['texto'],
        texto_html=data['texto_html'],
        comentario=data['comentario'],
        parrafo_id=data['parrafo_id'],
        usuario_id=data['usuario_id'],
        consolidar=data['consolidar'],
        permite=data['permite']
    )
    guardar_cambios(nueva_anotacion)

    for valor in data['valores']:
        nuevo_valor_anotacion = AnotacionValorRelacion(
            anotacion_id=nueva_anotacion.id,
            valor_id=valor['valor_id']
        )
        guardar_cambios(nuevo_valor_anotacion)

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
        AnotacionValorRelacion.query.filter_by(anotacion_id=id).delete()
        Anotacion.query.filter_by(id=id).delete()
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


def consultar_inconsistencia_notificacion(data):
    valor_consistente = []
    anotaciones_usuarios = (db.session.query(Anotacion, AnotacionValorRelacion)
                            .outerjoin(AnotacionValorRelacion, Anotacion.id == AnotacionValorRelacion.anotacion_id)
                            .filter(Anotacion.parrafo_id == data['parrafo_id'],
                                    Anotacion.permite == data['permite'],
                                    Anotacion.usuario_id != data['usuario_id']))

    for valor in data['valores']:
        if any(x[1].valor_id == valor['valor_id'] for x in anotaciones_usuarios):
            valor_consistente.append(True)
        else:
            valor_consistente.append(False)
    inconsistencia = AnotacionNotificacionConsultar(not all(x == True for x in valor_consistente))
    print(inconsistencia)
    return marshal(inconsistencia, AnotacionDto.anotacionNotificacionConsultar), 201


def obtener_total_anotaciones_parrafo_anotador(data):
    anotaciones_anotador_total = db.session.query(Anotacion)\
                                .filter(Anotacion.usuario_id == data['usuario_id'],
                                        Anotacion.parrafo_id == data['parrafo_id'],
                                        Anotacion.consolidar == data['consolidar']).count()
    respuesta = {
        'estado': 'exito',
        'num_anotaciones': anotaciones_anotador_total
    }
    return respuesta, 201


def obtener_anotacion_valores(anotacion_id):
    valores = [AnotacionValor]
    valores_anotaciones = (db.session.query(AnotacionValorRelacion, Valor, Atributo, Tratamiento)
                           .outerjoin(Valor, AnotacionValorRelacion.valor_id == Valor.id)
                           .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                           .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                           .filter(AnotacionValorRelacion.anotacion_id == anotacion_id)
                           .order_by(Tratamiento.id))

    valores.clear()
    j = 0
    for valor in valores_anotaciones:
        valor_aux = AnotacionValor()
        valores.insert(j, valor_aux)
        valores[j].valor_id = valor[1].id
        valores[j].valor_descripcion = valor[1].descripcion
        valores[j].atributo_descripcion = valor[2].descripcion
        valores[j].tratamiento_descripcion = valor[3].descripcion
        valores[j].color_primario = valor[3].color_tratamiento.codigo
        j += 1

    return valores


def obtener_anotaciones_parrafo_usuario(data):
    anotaciones = [AnotacionConsultarAnotador]
    anotaciones_consultar = (db.session.query(Anotacion)
                             .filter(Anotacion.parrafo_id == data['parrafo_id'],
                                     Anotacion.usuario_id == data['usuario_id'],
                                     Anotacion.consolidar == data['consolidar']).all())
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
            anotaciones.insert(i, item)
            anotaciones[i].valores = obtener_anotacion_valores(anotaciones[i].id)
            i += 1
        return marshal(anotaciones, AnotacionDto.anotacionConsultarAnotadores), 201


def consultar_ultima_anotacion_usuario_politica(politica_id, usuario_id, consolidar):
    ultimo_parrafo_anotado = (db.session.query(Anotacion.parrafo_id.distinct(), Parrafo, Politica)
                              .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                              .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                              .filter(Politica.id == politica_id,
                                      Anotacion.usuario_id == usuario_id,
                                      Anotacion.consolidar == consolidar).count())
    return ultimo_parrafo_anotado


def consultar_anotaciones_usuario(politica_id, secuencia, usuario_id, consolidar):
    anotaciones_usuario = [AnotacionConsultarAnotador]
    anotaciones_parrafo_usuarios = (db.session.query(Anotacion, Usuario, Parrafo)
                                    .outerjoin(Usuario, Anotacion.usuario_id == Usuario.id)
                                    .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                                    .filter(Parrafo.politica_id == politica_id,
                                            Parrafo.secuencia == secuencia,
                                            Anotacion.usuario_id == usuario_id,
                                            Anotacion.consolidar == consolidar).all())
    anotaciones_usuario.clear()
    i = 0
    if not anotaciones_parrafo_usuarios:
        return []
    else:
        for item in anotaciones_parrafo_usuarios:
            anotaciones_usuario.insert(i, item[0])
            anotaciones_usuario[i].valores = obtener_anotacion_valores(anotaciones_usuario[i].id)
            i += 1

        return anotaciones_usuario


def consultar_inconsistencia(politica_id, secuencia, usuarios):
    anotaciones_tuplas = []
    for usuario in usuarios:
        anotaciones_parrafo = (db.session.query(Anotacion, AnotacionValorRelacion, Valor, Atributo, Tratamiento, Parrafo)
                               .outerjoin(AnotacionValorRelacion, Anotacion.id == AnotacionValorRelacion.anotacion_id)
                               .outerjoin(Valor, AnotacionValorRelacion.valor_id == Valor.id)
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
            tupla = (anotacion[4].id, anotacion[3].id, anotacion[2].id, anotacion[0].permite)
            anotacion_usuario.insert(i, tupla)
            i += 1
        anotaciones_tuplas.append(anotacion_usuario)

    inconsistencia = not all(x == anotaciones_tuplas[0] for x in anotaciones_tuplas)

    return inconsistencia


def consultar_anotaciones_anotadores(data):
    usuarios_anotaciones = AnotacionesAnotadoresConsultarRespuesta
    anotaciones = [ConsultarAnotacionesAnotadoresParrafo]
    anotaciones_aux = []
    usuarios = (db.session.query(PoliticaUsuarioRelacion, Usuario, RolUsuario)
                .outerjoin(Usuario, PoliticaUsuarioRelacion.usuario_id == Usuario.id)
                .outerjoin(RolUsuario, Usuario.rol_usuario == RolUsuario.id)
                .filter(PoliticaUsuarioRelacion.politica_id == data['politica_id'],
                        PoliticaUsuarioRelacion.consolidar == False).all())

    i = 0
    anotaciones.clear()
    for usuario in usuarios:
        anotaciones.insert(i, usuario[1])
        anotaciones[i].rol_usuario = usuario[2].nombre
        anotaciones_aux.clear()
        anotaciones_aux = consultar_anotaciones_usuario(data['politica_id'], data['secuencia'], usuario[1].id, False)
        anotaciones[i].anotaciones = anotaciones_aux

    usuarios_anotaciones.inconsistencia = consultar_inconsistencia(data['politica_id'], data['secuencia'], usuarios)
    usuarios_anotaciones.usuarios_anotaciones = anotaciones

    return marshal(usuarios_anotaciones, AnotacionDto.anotacionesAnotadoresConsultarRespuesta), 201


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()