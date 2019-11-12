from app.main import db
from app.main.model.rol_usuario import RolUsuario
from app.main.model.modulo import Modulo
from ..util.dto import RolUsuarioDto
from flask_restplus import marshal


def guardar_nuevo_rol(data):
    rol = RolUsuario.query.filter_by(nombre=data['nombre']).first()
    if not rol:
        nuevo_rol = RolUsuario(
            nombre= data['nombre'],
            descripcion=data['descripcion']
        )
        guardar_cambios(nuevo_rol)
        response_object = {
            'estado': 'exito',
            'mensaje': 'Rol de usuario registrado exitosamente.'
        }
        return response_object,201
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'El rol de usuario ya existe'
        }
        return response_object, 409


def obtener_todos_roles():
    return RolUsuario.query.all()


def obtener_un_rol(id):
    return RolUsuario.query.filter_by(id=id).first()


def guardar_rol_modulo(data):
    rol = RolUsuario.query.filter_by(id=data['rol_id']).first()
    if rol:
        modulo = Modulo.query.filter_by(id=data['modulo_id']).first()
        if modulo:
            if modulo.padre_id == 1:
                rol.modulos += [modulo]
                guardar_cambios(rol)
                response_object = {
                    'estado': 'exito',
                    'mensaje': 'Modulo agregado a Rol de usuario exitosamente'
                }
                return response_object, 201
            else:
                response_object = {
                    'estado': 'fallido',
                    'mensaje': 'El modulo debe ser de PRIMER NIVEL para ser agregado a un Rol'
                }
                return response_object, 409
        else:
            response_object = {
                'estado': 'fallido',
                'mensaje': 'Modulo no encontrado'
            }
            return response_object, 409
    else:
        response_object = {
            'estado': 'fallido',
            'mensaje': 'Rol de usuario no encontrado'
        }
        return response_object, 409


def obtener_modulo_rol(rol_id):
    if rol_id == 0:
        rol_usuario = RolUsuario.query.all()
        return marshal(rol_usuario, RolUsuarioDto.rolUsuarioModuloCosultar)
    else:
        rol_usuario = RolUsuario.query.filter_by(id=rol_id).first()
        return marshal(rol_usuario, RolUsuarioDto.rolUsuarioModuloCosultar)


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()