from app.main import db
from app.main.model.valor import Valor
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.util.clases_auxiliares import ValorConsultar
from app.main.util.dto import ValorDto
from flask_restplus import marshal


_valorConsultar = ValorDto.valorConsultar


def guardar_valor(valor):
    valor_consultar = db.session.query(Valor)\
        .filter(Valor.descripcion == valor['descripcion'])\
        .filter(Valor.atributo_id == valor['atributo_id']).first()
    if not valor_consultar:
        nuevo_valor = Valor(
            descripcion= valor['descripcion'],
            atributo_id= valor['atributo_id']
        )
        guardar_cambios(nuevo_valor)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Atributo creado exitosamente'
        }
        return response_object, 201
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'La descripcion del valor ya existe para este atributo'
        }
        return response_object, 409


def obtener_todos_valores():
    valores = [ValorConsultar]
    valores_consultar = (db.session.query(Valor, Atributo, Tratamiento)
                         .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                         .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id).all())
    i = 0
    valores.clear()
    if not valores_consultar:
        respuesta = {
            'estado':'Fallido',
            'mensaje': 'No existen valores'
        }
        return respuesta, 404
    else:
        for item in valores_consultar:
            valores.insert(i, item[0])
            valores[i].tratamiento_id = item[2].id
            valores[i].color_primario = item[2].color_tratamiento.codigo
            i += 1
        return valores, 201


def obtener_valores_atributo(atributo_id):
    valores = [ValorConsultar]
    valores_consultar = (db.session.query(Valor, Atributo, Tratamiento)
                         .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                         .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                         .filter(Valor.atributo_id == atributo_id).all())
    i = 0
    valores.clear()
    if not valores_consultar:
        return 404
    else:
        for item in valores_consultar:
            valores.insert(i, item[0])
            valores[i].tratamiento_id = item[2].id
            valores[i].color_primario = item[2].color_tratamiento.codigo
            i += 1
        return valores, 201


def obtener_valores_atributo_completo(atributo_id):
    valores = [ValorConsultar]
    valores_consultar = (db.session.query(Valor, Atributo, Tratamiento)
                         .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                         .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                         .filter(Valor.atributo_id == atributo_id).all())
    i = 0
    valores.clear()
    for item in valores_consultar:
        valores.insert(i, item[0])
        valores[i].tratamiento_id = item[2].id
        valores[i].color_primario = item[2].color_tratamiento.codigo
        i += 1
    return valores


def obtener_valor(id):
    valor_aux = db.session.query(Valor, Atributo, Tratamiento)\
        .outerjoin(Atributo, Valor.atributo_id == Atributo.id)\
        .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)\
        .filter(Valor.id == id).first()
    if not valor_aux:
        respose_object = {
            'estatus': 'fallido',
            'mensaje': 'No exite atributo'
        }
        return respose_object,404
    else:
        valor = ValorConsultar
        valor.id = valor_aux[0].id
        valor.descripcion = valor_aux[0].descripcion
        valor.tratamiento_id = valor_aux[2].id
        valor.atributo_id = valor_aux[0].atributo_id
        valor.color_primario = valor_aux[2].color_tratamiento.codigo
        return marshal(valor, _valorConsultar), 201


def obtener_valor_completo(valor_id):
    valor_aux = db.session.query(Valor, Atributo, Tratamiento)\
        .outerjoin(Atributo, Valor.atributo_id == Atributo.id)\
        .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)\
        .filter(Valor.id == valor_id).first()
    if not valor_aux:
        respose_object = {
            'estatus': 'fallido',
            'mensaje': 'No exite atributo'
        }
        return respose_object,404
    else:
        print(valor_aux[2])
        valor = ValorConsultar
        valor.id = valor_aux[0].id
        valor.descripcion = valor_aux[0].descripcion
        valor.tratamiento_id = valor_aux[2].id
        valor.tratamiento_descripcion = valor_aux[2].descripcion
        valor.atributo_id = valor_aux[1].id
        valor.atributo_descripcion = valor_aux[1].descripcion
        valor.color_primario = valor_aux[2].color_tratamiento.codigo
        return marshal(valor, ValorDto.valorConsultarCompleto), 201


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()