from app.main import db
from app.main.model.valor import Valor
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.util.clases_auxiliares import ValorConsultar
from app.main.util.dto import ValorDto
from flask_restplus import marshal


_valorConsultar = ValorDto.valorConsultar


def guardar_valor(valor):
    valor_consultar = (db.session.query(Valor)
                       .filter(Valor.descripcion == valor['descripcion'])
                       .filter(Valor.atributo_id == valor['atributo_id']).first())
    if not valor_consultar:
        nuevo_valor = Valor(
            descripcion= valor['descripcion'],
            atributo_id= valor['atributo_id']
        )
        guardar_cambios(nuevo_valor)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Atributo creado exitosamente'
        }
        return respuesta, 201
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'La descripcion del valor ya existe para este atributo'
        }
        return respuesta, 409


def editar_valor(data):
    valor = Valor.query.filter_by(id=data['id']).first()
    if not valor:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el valor'
        }
        return respuesta, 409
    else:
        valor.descripcion = data['descripcion']
        guardar_cambios(valor)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Atributo editado exitosamente'
        }
        return respuesta, 201


def eliminar_valor(id):
    try:
        Valor.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el valor'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Atributo eliminado exitosamente'
        }
        return respuesta, 201


def obtener_valores_atributo(atributo_id):
    """ Obtiene los valores que pertenecen a un atributo"""
    valores = [ValorConsultar]
    valores_consultar = (db.session.query(Valor, Atributo, Tratamiento)
                         .outerjoin(Atributo, Valor.atributo_id == Atributo.id)
                         .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)
                         .filter(Valor.atributo_id == atributo_id).all())
    i = 0
    valores.clear()
    if not valores_consultar:
        return [], 201
    else:
        for item in valores_consultar:
            valores.insert(i, item[0])
            valores[i].tratamiento_id = item[2].id
            valores[i].color_primario = item[2].color_tratamiento.codigo
            i += 1
        return marshal(valores, ValorDto.valorConsultar) , 201


def obtener_valores_atributo_completo(atributo_id):
    """ Obtiene los valores de un atributo pero incluyendo el id de atributo y tratamiento padre y
        el color del tratamiento. Esta función es útil para presentar la vista de árbol de las herramientas de
        anotación y visualización"""
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


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
