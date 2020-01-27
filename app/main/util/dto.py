from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='operaciones relaciones a autenticacion')
    usuario_auth = api.model('detalles_auth', {
        'email': fields.String(required=True, description='email de usuario'),
        'clave': fields.String(required=True, description='clave del usuario'),
    })


class ColorDto:

    api = Namespace('Color', description='Operaciones relacionadas a paleta de colores para anotaciones')
    color = api.model('color',{
        'codigo': fields.String(required=True, description='codigo hexadecimal del color')
    })

    colorConsultar = api.model('colorConsultar',{
        'id': fields.Integer(required=True, descripcion='id del color'),
        'codigo': fields.String(description='codigo hexadecimal del color'),
        'disponible': fields.Boolean(description='color disponible')
    })


class ModuloDto:
    api = Namespace('Modulo', description='Operaciones relacionadas a modulos')
    modulo = api.model('modulo',{
        'nombre': fields.String(required=True, description='nombre del modulo(unico)'),
        'icono' : fields.String(required=True, description='icono para menu'),
        'padre_id' : fields.Integer(required=True, description='id del modulo padre, NULL para modulo sin padre')
    })

    moduloConsultar = api.model('moduloConsultar', {
        'id' : fields.Integer (required = True, description ='id del modulo'),
        'nombre': fields.String(required=True, description='nombre del modulo'),
        'icono': fields.String(required=True, description='icono para menu'),
        'padre_id': fields.Integer(required=True, description='id del modulo padre')
    })

    moduloConsultarHijos = api.model('moduloConsultarHijos', {
        'nombre': fields.String(required=True, description='nombre del modulo'),
        'icono': fields.String(required=True, description='icono para menu'),
        'hijos': fields.List(fields.Nested(api.model('hijos',{
            'nombre': fields.String(required=True, description='nombre del modulo'),
            'icono': fields.String(required=True, description='icono para menu'),
        })))
    })

    moduloConsultarHijos2 = api.inherit('moduloConsultarHijos2', moduloConsultarHijos, {
        'hijos': fields.List(fields.Nested(moduloConsultarHijos))
    })


class PoliticaDto:
    api = Namespace('Politica', description='Operaciones relacionadas a politicas')
    politica = api.model('Politica', {
        'nombre': fields.String(required=True, description='Nombre de la empresa o compania'),
        'url': fields.String(required=True, description='URL del sitio de donde se obtuvo la politica'),
        'fecha': fields.Date(required=True, description='Fecha en la cual fue publicada la politica de privacidad')
    })


class RolUsuarioDto:
    api = Namespace('RolUsuario', description='Operaciones relacionadas a roles de usuario')
    rolUsuario = api.model('rolUsuario', {
        'nombre': fields.String(required=True, description= 'nombre del rol de usuario'),
        'descripcion': fields.String(required=True, description = 'descripcion del rol en el sistema')
    })

    rolUsuarioConsultar = api.model ('rolUsuarioConsultar', {
        'id' : fields.Integer(required = True, description = 'id del rol'),
        'nombre': fields.String(required=True, description='nombre del rol de usuario'),
        'descripcion': fields.String(required=True, description='descripcion del rol en el sistema')
    })

    rolUsuarioModulo = api.model('rolUsuarioModulo',{
        'rol_id': fields.Integer(required = True, description = 'id del rol de usuario'),
        'modulo_id':  fields.Integer(required = True, description = 'id del modulo asignado al rol')
    })

    rolUsuarioModuloCosultar = api.model('rolUsuarioModuloCosultar',{
        'id': fields.Integer(required=True, description='id del rol'),
        'nombre': fields.String(required=True, description='nombre del rol de usuario'),
        'descripcion': fields.String(required=True, description='descripcion del rol en el sistema'),
        'modulos': fields.List(fields.Nested(ModuloDto.moduloConsultarHijos2))
    })


class UsuarioDto:
    api = Namespace('Usuario', description='Operaciones relacionadas a usuarios ')
    usuario = api.model('usuario',{
        'email': fields.String(required=True, description='direccion de email de usuario/nombre de usuario'),
        'clave': fields.String(required=True, description='clave para la cuenta del usuario'),
        'rol_usuario': fields.Integer(required=True, description='rol de usuario'),
        'entrenamiento': fields.Boolean(required=True, description='el usuario sera sometido a entrenamiento?')
    })

    usuarioConsultar = api.model('usuarioConsultar', {
        'id': fields.Integer(description='id de usuario'),
        'email': fields.String(required=True, description='direccion de email de usuario/nombre de usuario'),
        'rol_usuario': fields.String(required=True, description='rol de usuario'),
        'activo': fields.Boolean(description='Usuario activo/inactivo'),
        'entrenamiento': fields.Boolean(description='Usuario en entrenamiento?')
    })

    usuarioConsultarLogin = api.model('usuarioConsultarLogin',{
        'id': fields.Integer(description='id de usuario'),
        'email': fields.String(required=True, description='direccion de email de usuario/nombre de usuario'),
        'rol_usuario': fields.String(required=True, description='rol de usuario'),
        'activo': fields.Boolean(description='Usuario activo/inactivo'),
        'entrenamiento': fields.Boolean(description='Usuario en entrenamiento?'),
        'modulos': fields.List(fields.Nested(ModuloDto.moduloConsultarHijos2))

    })


class ValorDto:
    api = Namespace('Valor', description='Operaciones relacionadas a valores de un atributo')
    valor = api.model('valor', {
        'descripcion': fields.String(required=True, description='nombre del valor'),
        'atributo_id': fields.Integer(requried=True, description='id del atributo padre'),
    })

    valorConsultar = api.model('valorConsultar', {
        'id': fields.Integer(required=True, description='id del atributo'),
        'descripcion': fields.String(required=True, description='nombre del valor'),
        'tratamiento_id': fields.Integer(required=True, description='id del tratamiento padre'),
        'atributo_id': fields.Integer(required=True, description='id del atributo padre'),
        'color_primario': fields.String(requried=True, description='codigo hexadecimal del color')
    })

    valorCompleto = api.model('valorCompleto', {
        'id': fields.Integer(required=True, description='id del atributo'),
        'descripcion': fields.String(required=True, description='nombre del valor'),
        'color_primario': fields.String(requried=True, description='codigo hexadecimal del color')
    })


class AtributoDto:
    api = Namespace('Atributo', description='Operaciones relacionadas a atributos de tratamientos de datos')
    atributo = api.model('atributo', {
        'descripcion': fields.String(required=True, description='nombre del atributo'),
        'tratamiento_id': fields.String(requried=True, description='id del tratamiento padre')
    })

    atributoConsultar = api.model('atributoConsultar', {
        'id': fields.Integer(required=True, description ='id del atributo'),
        'descripcion': fields.String(required=True, description='nombre del atributo'),
        'tratamiento_id': fields.Integer(requried=True, description='id del tratamiento padre'),
        'color_primario': fields.String(requried=True, description='codigo hexadecimal del color')
    })

    atributoCompleto = api.model('atributoCompleto', {
        'id': fields.Integer(required=True, description='id del atributo'),
        'descripcion': fields.String(required=True, description='nombre del atributo'),
        'color_primario': fields.String(requried=True, description='codigo hexadecimal del color'),
        'hijos': fields.List(fields.Nested(ValorDto.valorCompleto))

    })


class TratamientoDto:
    api = Namespace('Tratamiento', description='Operaciones relacionadas a tratamientos')
    tratamiento = api.model('tratamiento',{
        'descripcion': fields.String(required=True, description='descripcion del tratamiento'),
        'color_primario': fields.Integer(required=True, description='id del color')
    })

    tratamientoConsultar = api.model('tratamientoConsultar', {
        'id': fields.Integer(required=False, description='id tratamiento'),
        'descripcion': fields.String(required=True, description='descripcion del tratamiento'),
        'color_primario': fields.String(required=True, description='Color del tratamiento para anotaciones')
    })

    tratamientoCompleto = api.model('tratamientoCompleto', {
        'id': fields.Integer(required=True),
        'descripcion': fields.String(required=True, description='descripcion del tratamiento'),
        'color_primario': fields.String(required=True, description='Color del tratamiento para anotaciones'),
        'hijos': fields.List(fields.Nested(AtributoDto.atributoCompleto))
    })



