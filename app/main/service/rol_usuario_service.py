from app.main import db
from app.main.model.rol_usuario import RolUsuario
from app.main.model.modulo import Modulo
from ..util.dto import RolUsuarioDto
from flask_restplus import marshal


def guardar_rol(rol):
    rol_aux = RolUsuario.query.filter_by(nombre=rol['nombre']).first()
    if not rol_aux:
        nuevo_rol = RolUsuario(
            nombre=rol['nombre'],
            descripcion=rol['descripcion']
        )
        guardar_cambios(nuevo_rol)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Rol de usuario registrado exitosamente.'
        }
        return respuesta, 201
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'El rol de usuario ya existe'
        }
        return respuesta, 409


def editar_rol(rol):
    rol_aux = RolUsuario.query.filter_by(id=rol['id']).first()
    if not rol_aux:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el rol de usuario'
        }
        return respuesta, 409
    else:
        rol_aux.nombre = rol['nombre']
        rol_aux.descripcion = rol['descripcion']
        guardar_cambios(rol_aux)
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Rol de usuario editado exitosamente'
        }
        return respuesta, 201


def eliminar_rol(id):
    try:
        RolUsuario.query.filter_by(id=id).delete()
    except:
        db.session.rollback()
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'No existe el rol de usuario'
        }
        return respuesta, 409
    else:
        db.session.commit()
        respuesta = {
            'estado': 'exito',
            'mensaje': 'Rol de usuario eliminado exitosamente'
        }
        return respuesta, 201


def obtener_roles():
    return RolUsuario.query.all()


def obtener_rol(id):
    return RolUsuario.query.filter_by(id=id).first()


def guardar_rol_modulo(modulo):
    """ Guarda la relación de un módulo con un rol de usuario """
    rol = RolUsuario.query.filter_by(id=modulo['rol_id']).first()
    if rol:
        modulo = Modulo.query.filter_by(id=modulo['modulo_id']).first()
        if modulo:
            if modulo.padre_id == 1:
                rol.modulos += [modulo]
                guardar_cambios(rol)
                respuesta = {
                    'estado': 'exito',
                    'mensaje': 'Modulo agregado a Rol de usuario exitosamente'
                }
                return respuesta, 201
            else:
                respuesta = {
                    'estado': 'fallido',
                    'mensaje': 'El modulo debe ser de PRIMER NIVEL para ser agregado a un Rol'
                }
                return respuesta, 409
        else:
            respuesta = {
                'estado': 'fallido',
                'mensaje': 'Modulo no encontrado'
            }
            return respuesta, 409
    else:
        respuesta = {
            'estado': 'fallido',
            'mensaje': 'Rol de usuario no encontrado'
        }
        return respuesta, 409


def guardar_cambios(data):
    db.session.add(data)
    db.session.commit()
