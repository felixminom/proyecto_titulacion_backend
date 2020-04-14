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
from app.main.util.clases_auxiliares import AnotacionConsultarAnotador, ConsultarAnotacionesAnotadoresParrafo, \
    AnotacionesAnotadoresConsultarRespuesta, AnotacionValor, AnotacionNotificacionConsultar, AnotacionesUsuarioDetalle,\
    DetallesAnotacionPolitica
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


def valor_notificacion(valor_id):
    valor = (db.session.query(Valor, Atributo, Tratamiento)
             .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
             .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
             .filter(Valor.id == valor_id).first())

    return valor


def consultar_inconsistencia_notificacion(data):
    anotaciones_usuarios = (db.session.query(Anotacion, AnotacionValorRelacion, Valor, Atributo, Tratamiento)
                            .outerjoin(AnotacionValorRelacion, Anotacion.id == AnotacionValorRelacion.anotacion_id)
                            .outerjoin(Valor, AnotacionValorRelacion.valor_id == Valor.id)
                            .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                            .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                            .filter(Anotacion.parrafo_id == data['parrafo_id'],
                                    Anotacion.permite == data['permite'],
                                    Anotacion.usuario_id != data['usuario_id'])
                            .order_by(Tratamiento.id).all())

    if not anotaciones_usuarios:
        parrafo_secuencia = (db.session.query(Parrafo)
                             .filter(Parrafo.id == data['parrafo_id']).first())

        usuarios_anotadores = (db.session.query(PoliticaUsuarioRelacion,)
                               .outerjoin(Politica, PoliticaUsuarioRelacion.politica_id == Politica.id)
                               .outerjoin(Parrafo, Politica.id == Parrafo.politica_id)
                               .filter(PoliticaUsuarioRelacion.consolidar == False,
                                       Parrafo.id == data['parrafo_id'],
                                       PoliticaUsuarioRelacion.usuario_id != data['usuario_id']).all())

        usuarios_ultimo_parrafo = []

        for politica_usuario in usuarios_anotadores:
            usuarios_ultimo_parrafo.append(consultar_ultima_anotacion_usuario_politica(politica_usuario.politica_id,
                                                                                       politica_usuario.usuario_id,
                                                                                       False))

        i = 0
        valores_no_consistentes = []
        for valor in data['valores']:
            valor = valor_notificacion(valor['valor_id'])
            valores_no_consistentes.insert(i, valor[0])
            valores_no_consistentes[i].valor_id = valor[0].id
            valores_no_consistentes[i].valor_descripcion = valor[0].descripcion
            valores_no_consistentes[i].atributo_descripcion = valor[1].descripcion
            valores_no_consistentes[i].tratamiento_descripcion = valor[2].descripcion
            valores_no_consistentes[i].color_primario = valor[2].color_tratamiento.codigo
            i += 1

        notificacion = AnotacionNotificacionConsultar(any(x > parrafo_secuencia.secuencia
                                                      for x in usuarios_ultimo_parrafo),
                                                      valores_no_consistentes,
                                                      [])

        return marshal(notificacion, AnotacionDto.anotacionNotificacionConsultar), 201
    else:
        consistencia_valores = []
        valores_no_consistentes = []
        valores_sugeridos = []
        i = 0
        for valor in data['valores']:
            if any(x[1].valor_id == valor['valor_id'] for x in anotaciones_usuarios):
                consistencia_valores.append(True)
            else:
                consistencia_valores.append(False)
                valor = valor_notificacion(valor['valor_id'])
                valores_no_consistentes.insert(i, valor[0])
                valores_no_consistentes[i].valor_id = valor[0].id
                valores_no_consistentes[i].valor_descripcion = valor[0].descripcion
                valores_no_consistentes[i].atributo_descripcion = valor[1].descripcion
                valores_no_consistentes[i].tratamiento_descripcion = valor[2].descripcion
                valores_no_consistentes[i].color_primario = valor[2].color_tratamiento.codigo
                i += 1

        inconsistencia = not all(x for x in consistencia_valores)

        if inconsistencia:
            i = 0
            for valor in anotaciones_usuarios:
                valores_sugeridos.insert(i, valor[2])
                valores_sugeridos[i].valor_id = valor[2].id
                valores_sugeridos[i].valor_descripcion = valor[2].descripcion
                valores_sugeridos[i].atributo_descripcion = valor[3].descripcion
                valores_sugeridos[i].tratamiento_descripcion = valor[4].descripcion
                valores_sugeridos[i].color_primario = valor[4].color_tratamiento.codigo
                i += 1

        valores_sugeridos_unicos = lista_unica(valores_sugeridos)

        notificacion = AnotacionNotificacionConsultar(inconsistencia,
                                                      valores_no_consistentes,
                                                      valores_sugeridos_unicos)

        return marshal(notificacion, AnotacionDto.anotacionNotificacionConsultar), 201


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
    valores = []
    valores_anotaciones = (db.session.query(AnotacionValorRelacion, Valor, Atributo, Tratamiento)
                           .outerjoin(Valor, AnotacionValorRelacion.valor_id == Valor.id)
                           .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                           .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                           .filter(AnotacionValorRelacion.anotacion_id == anotacion_id)
                           .order_by(Tratamiento.id))

    valores.clear()
    i = 0
    for valor in valores_anotaciones:
        valor_aux = AnotacionValor()
        valores.insert(i, valor_aux)
        valores[i].valor_id = valor[1].id
        valores[i].valor_descripcion = valor[1].descripcion
        valores[i].atributo_descripcion = valor[2].descripcion
        valores[i].tratamiento_descripcion = valor[3].descripcion
        valores[i].color_primario = valor[3].color_tratamiento.codigo
        i += 1

    return valores


def obtener_anotaciones_parrafo_usuario(data):
    anotaciones = []
    anotaciones_consultar = (db.session.query(Anotacion)
                             .filter(Anotacion.parrafo_id == data['parrafo_id'],
                                     Anotacion.usuario_id == data['usuario_id'],
                                     Anotacion.consolidar == data['consolidar']).all())

    if not anotaciones_consultar:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'no existen anotaciones para este parrafo'
        }
        return respuesta, 404
    else:
        i = 0
        for item in anotaciones_consultar:
            anotaciones.insert(i, item)
            anotaciones[i].valores = obtener_anotacion_valores(anotaciones[i].id)
            i += 1
        return marshal(anotaciones, AnotacionDto.anotacionConsultarAnotadores), 201


def consultar_ultima_anotacion_usuario_politica(politica_id, usuario_id, consolidar):
    ultimo_parrafo_anotado = (db.session.query(Anotacion.parrafo_id, Parrafo.secuencia)
                              .outerjoin(AnotacionValorRelacion,)
                              .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                              .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                              .filter(Politica.id == politica_id,
                                      Anotacion.usuario_id == usuario_id,
                                      Anotacion.consolidar == consolidar)
                              .order_by(Parrafo.secuencia.desc()).first())

    if ultimo_parrafo_anotado:
        return ultimo_parrafo_anotado[1]
    else:
        return -1


def consultar_anotaciones_usuario(politica_id, secuencia, usuario_id, consolidar):
    anotaciones_usuario = []
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
    anotaciones = []
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


#Calculo de coeficiente interanotador
def consultar_detalles_anotacion_politica(data):
    detallesPolitica = DetallesAnotacionPolitica
    detallesPolitica.anotadores = []
    usuarios = (db.session.query(PoliticaUsuarioRelacion, Usuario)
                .outerjoin(Usuario, PoliticaUsuarioRelacion.usuario_id == Usuario.id)
                .filter(PoliticaUsuarioRelacion.politica_id == data['politica_id'],
                        PoliticaUsuarioRelacion.consolidar == False).all())

    detallesPolitica.coeficiente = calcular_coeficiente_interanotador(data['politica_id'], usuarios)
    for usuario in usuarios:
        usuarioAux = AnotacionesUsuarioDetalle()
        usuarioAux.email = usuario[1].email
        usuarioAux.total_anotaciones = consultar_total_anotaciones_usuario(data['politica_id'], usuario[1].id, False)
        detallesPolitica.anotadores.append(usuarioAux)

    return marshal(detallesPolitica, AnotacionDto.detallesAnotacionPolitica), 201


def consultar_total_anotaciones_usuario(politica_id, usuario_id, consolidar):
    total_anotaciones = (db.session.query(Anotacion)
                         .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                         .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                         .filter(Politica.id == politica_id,
                                 Anotacion.usuario_id == usuario_id,
                                 Anotacion.consolidar == consolidar).count())

    return total_anotaciones


def calcular_coeficiente_interanotador(politica_id, usuarios):
    listaAnotaciones = []

    for usuario in usuarios:
        valores = (db.session.query(Anotacion.permite.distinct(), AnotacionValorRelacion.valor_id)
                   .outerjoin(AnotacionValorRelacion, Anotacion.id == AnotacionValorRelacion.anotacion_id)
                   .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                   .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                   .filter(Politica.id == politica_id,
                           Anotacion.usuario_id == usuario[1].id,
                           Anotacion.consolidar == False))

        for valor in valores:
            tupla = (valor[0], valor[1])
            listaAnotaciones.append(tupla)

    acumulador = 0
    lista_anotaciones_unica = lista_unica(listaAnotaciones)
    for anotacion in listaAnotaciones:
        acumulador = acumulador + listaAnotaciones.count(anotacion) - 1
        listaAnotaciones = [ant for ant in listaAnotaciones if ant != anotacion]

        if not listaAnotaciones:
            # anotacionesSimilares / (anotaciones_diferentes_por_numero_usuarios)
            coeficiente = (acumulador/(len(lista_anotaciones_unica)*(len(usuarios)-1))) *100
            return coeficiente


def lista_unica(lista):
    lista_unica = []
    for x in lista:
        if x not in lista_unica:
            lista_unica.append(x)

    return lista_unica


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()