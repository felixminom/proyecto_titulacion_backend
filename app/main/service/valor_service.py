from app.main import db
from app.main.model.valor import Valor
from app.main.model.atributo import Atributo
from app.main.model.tratamiento import Tratamiento
from app.main.util.clases_auxiliares import ValorConsultar


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
        return 404
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


def obtener_valor(id):
    valor = db.session.query(Valor, Atributo, Tratamiento)\
        .outerjoin(Atributo, Valor.atributo_id == Atributo.id)\
        .outerjoin(Tratamiento, Atributo.tratamiento_id == Tratamiento.id)\
        .filter(Valor.id == id).first()
    if not valor:
        return 404
    else:
        return valor, 201


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()