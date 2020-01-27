class ModuloConsultarHijos:
    def __init__(self, nombre, icono, hijos):
        self.nombre = nombre
        self.icono = icono
        self.hijos = hijos


class UsuarioConsultar:
    def __init__(self, id, email, rol_usuario, activo, entrenamiento):
        self.id = id
        self.email = email
        self.rol_usuario = rol_usuario
        self.activo = activo
        self.entrenamiento = entrenamiento


class UsuarioConsultarLogin:
    def __init__(self, id, email, rol_usuario, activo, modulos):
        self.id = id
        self.email = email
        self.rol_usuario = rol_usuario
        self.activo = activo
        self.modulos = modulos


class TratamientoConsultar:
    def __init__(self, id, descripcion):
        self.id = id
        self.descripcion = descripcion
        self.color_primario = ''

    def __init__(self, id, descripcion, color_primario):
        self.id = id
        self.descripcion = descripcion
        self.color_primario = color_primario


class AtributoCompleto:
    def __init__(self, id, descripcion, color_primario, hijos):
        self.id = id
        self.descripcion = descripcion
        self.color_primario = color_primario
        self.hijos = hijos


class TratamientoCompleto:
    def __init__(self, id, descripcion, color_primario, hijos):
        self.id = id
        self.descripcion = descripcion
        self.color_primario = color_primario
        self.hijos = hijos


class AtributoConsultar:
    def __init__(self, id, descripcion, tratamiento_id, color_primario):
        self.id = id,
        self.descripcion = descripcion,
        self.tratamiento_id = tratamiento_id,
        self.color_primario = color_primario


class ValorConsultar:
    def __init__(self, id, descripcion, tratamiento_id, atributo_id, color_primario):
        self.id = id,
        self.descripcion = descripcion,
        self.tratamiento_id = tratamiento_id,
        self.atributo_id = atributo_id
        self.color_primario = color_primario
