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
from app.main.util.clases_auxiliares import AnotacionesAnotadoresConsultarRespuesta, AnotacionValor, \
    AnotacionNotificacionConsultar, AnotacionesUsuarioDetalle,\
    DetallesAnotacionPolitica
from app.main.service.parrafo_service import consultar_num_parrafos_politica
from flask_restplus import marshal
import datetime
from numpy import array
import krippendorff

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
        ejecuta=data['ejecuta']
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
        anotacion.ejecuta = data['ejecuta']
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
                                    Anotacion.ejecuta == data['ejecuta'],
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
                                                      for x in usuarios_ultimo_parrafo) or
                                                      any(x.finalizado == True for x in usuarios_anotadores),
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
        return [], 201
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
        anotaciones_parrafo = (db.session.query(Anotacion, AnotacionValorRelacion)
                               .outerjoin(AnotacionValorRelacion, Anotacion.id == AnotacionValorRelacion.anotacion_id)
                               .outerjoin(Valor, AnotacionValorRelacion.valor_id == Valor.id)
                               .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                               .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                               .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                               .filter(Parrafo.politica_id == politica_id,
                                       Parrafo.secuencia == secuencia,
                                       Anotacion.usuario_id == usuario[1].id,
                                       Anotacion.consolidar == False)
                               .order_by(AnotacionValorRelacion.valor_id).all())
        i = 0
        anotacion_usuario = []
        for anotacion in anotaciones_parrafo:
            tupla = (anotacion[1].valor_id, anotacion[0].ejecuta)
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

    politica = Politica.query.filter_by(id=data['politica_id']).first()

    detallesPolitica.coeficiente = politica.coeficiente

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
    lista_anotaciones_usuarios = []

    # Se consulta los valores que han sido anotadas sobre la política por cada usuario
    for usuario in usuarios:
        valores = (db.session.query(Anotacion.ejecuta.distinct(), AnotacionValorRelacion.valor_id)
                   .outerjoin(AnotacionValorRelacion, Anotacion.id == AnotacionValorRelacion.anotacion_id)
                   .outerjoin(Parrafo, Anotacion.parrafo_id == Parrafo.id)
                   .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                   .filter(Politica.id == politica_id,
                           Anotacion.usuario_id == usuario[1].id,
                           Anotacion.consolidar == False)
                   .order_by(AnotacionValorRelacion.valor_id).all())

        #Se crea una tupla (valor.id, anotacion.ejecuta) por cada valor anotado
        anotaciones_usuario = []

        for valor in valores:
            tupla = (valor[0], valor[1])
            anotaciones_usuario.append(tupla)

        #Se adjunta a lista_anotaciones_usuarios los valores encontrados en este usuario.
        #Una vez que se realiza el ciclo para todos los usuarios se obtendrán todos
        #los valores que han sido anotados sobre la política
        lista_anotaciones_usuarios.append(anotaciones_usuario)

    #Esta variable contiene todos los valores anotados sobre la política
    #Se eliminan tuplas repetidas
    lista_unica_anotaciones = lista_anidada_unica(lista_anotaciones_usuarios)

    #Se inicializa la matriz de datos de confiabilidad
    matriz_datos_confiabilidad = []

    #Se verifica que valores existen en cada usuario
    #se añade un 1 en caso que el valor existe
    #o un 0 en caso negativo.
    for usuario in lista_anotaciones_usuarios:
        datos_usuario = []
        for valor in lista_unica_anotaciones:
            if valor in usuario:
                datos_usuario.append(1)
            else:
                datos_usuario.append(0)
        matriz_datos_confiabilidad.append(datos_usuario)

    #Se consulta en la bdd cuantos parrafos de la política contienen anotaciones
    numero_parrafos_anotados = (db.session.query(Parrafo.id.distinct())
                                .outerjoin(Anotacion, Parrafo.id == Anotacion.parrafo_id)
                                .outerjoin(Politica, Parrafo.politica_id == Politica.id)
                                .filter(Anotacion.consolidar == False,
                                        Politica.id == politica_id).count())

    numero_parrafos_totales = consultar_num_parrafos_politica(politica_id)

    #Se calcula el numero de párafos no anotados
    numero_parrafos_no_anotados= numero_parrafos_totales - numero_parrafos_anotados

    #Por cada parrafo no anotado se añade un 0
    #en todos las filas de la matriz de datos de confiablidad
    if numero_parrafos_no_anotados == 0:
        if all(x == matriz_datos_confiabilidad[0] for x in matriz_datos_confiabilidad):
            for usuario in matriz_datos_confiabilidad:
                usuario.append(0)
    else:
        for i in range(0, numero_parrafos_no_anotados):
            for usuario in matriz_datos_confiabilidad:
                usuario.append(0)

    #Se transforma la matriz de datos de confiabilidad a un array que la librería
    #kirppendorff puede entender
    datos_de_fiabilidad = array(matriz_datos_confiabilidad)

    #Cálculo del coeficiente mediante la librería
    return krippendorff.alpha(reliability_data=datos_de_fiabilidad, level_of_measurement='nominal')


def lista_unica(lista):
    lista_unica = []
    for x in lista:
        if x not in lista_unica:
            lista_unica.append(x)

    return lista_unica


def lista_anidada_unica(lista_listas):
    lista_unica = []
    for lista in lista_listas:
        for x in lista:
            if x not in lista_unica:
                lista_unica.append(x)
    return lista_unica


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
