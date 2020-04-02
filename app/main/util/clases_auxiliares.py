class ModuloConsultarHijos:
    def __init__(self, nombre, icono, path, hijos):
        self.nombre = nombre
        self.icono = icono
        self.path = path
        self.hijos = hijos


class UsuarioConsultar:
    def __init__(self, id, email, rol_usuario_id, rol_usuario, activo, entrenamiento):
        self.id = id
        self.email = email
        self.rol_usuario_id = rol_usuario_id
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

    def __init__(self, id, descripcion, color_id, color_primario_codigo):
        self.id = id
        self.descripcion = descripcion
        self.color_id = color_id
        self.color_primario_codigo = color_primario_codigo


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
        self.id = id
        self.descripcion = descripcion
        self.tratamiento_id = tratamiento_id
        self.color_primario = color_primario


class ValorConsultar:
    def __init__(self, id, descripcion, tratamiento_id, atributo_id, color_primario):
        self.id = id
        self.descripcion = descripcion
        self.tratamiento_id = tratamiento_id
        self.atributo_id = atributo_id
        self.color_primario = color_primario


class ValorConsultarCompleto:
    def __init__(self, id, descripcion, atributo_id, atributo_descripcion, tratamiento_id, tratamiento_descripcion, color_primario):
        self.id = id
        self.color_primario = color_primario
        self.descripcion = descripcion
        self.atributo_id = atributo_id
        self.atributo_descripcion = atributo_descripcion
        self.tratamiento_id = tratamiento_id
        self.tratamiento_descripcion = tratamiento_descripcion


class ParrafoMostrar:
    def __init__(self, titulo='', texto='', texto_html=''):
        self.titulo = titulo
        self.texto = texto
        self.texto_html = texto_html


class ParrafoGuardar:
    def __init__(self, secuencia, titulo, texto, texto_html, politica_id):
        self.secuencia = secuencia
        self.titulo = titulo
        self.texto = texto
        self.texto_html = texto_html
        self.politica_id = politica_id


class PoliticaMostrar:
    def __init__(self, nombre ='', fecha='', url='', parrafos=[]):
        self.nombre = nombre
        self.fecha = fecha
        self.url = url
        self.parrafos = parrafos


class AnotacionesUsuarioDetalle:
    def __init__(self, email ='', total_anotaciones=0):
        self.email = email
        self.total_anotaciones = total_anotaciones


class DetallesAnotacionPolitica:
    def __init__(self, coeficiente, anotadores):
        self.coeficiente = coeficiente
        self.anotadores = anotadores


class AnotacionNotificacionConsultar:
    def __init__(self, inconsistencia):
        self.inconsistencia = inconsistencia


class AnotacionConsultar:
    def __init__(self, texto, texto_html, comentario, valor_id, valor_descripcion, atributo_id, atributo_descripcion,
                tratamiento_id, tratamiento_descripcion, parrafo_id, usuario_id, usuario_nombre):
        self.texto = texto
        self.texto_html = texto_html
        self.comentario = comentario
        self.valor_id = valor_id
        self.valor_descripcion = valor_descripcion
        self.atributo_id = atributo_id
        self.atributo_descripcion = atributo_descripcion
        self.tratamiento_id = tratamiento_id
        self.tratamiento_descripcion = tratamiento_descripcion
        self.parrafo_id = parrafo_id
        self.usuario_id = usuario_id
        self.usuario_nombre = usuario_nombre


class AnotacionValor:
    def __init__(self, valor_id = 0, valor_descripcion ='', atributo_descripcion='', tratamiento_descripcion='',
                 color_primario =''):
        self.valor_id = valor_id
        self.valor_descripcion = valor_descripcion
        self. atributo_descripcion = atributo_descripcion
        self. tratamiento_descripcion = tratamiento_descripcion
        self.color_primario = color_primario


class AnotacionConsultarAnotador:
    def __init__(self, id, texto, comentario, valores):
        self.id = id
        self.texto = texto
        self.comentario = comentario
        self.valores = valores


class ConsultarAnotacionesAnotadoresParrafo:
    def __init__(self, usuario_email, rol_usuario, anotaciones):
        self.email = usuario_email
        self.rol_usuario = rol_usuario
        self.anotaciones = anotaciones


class AnotacionesAnotadoresConsultarRespuesta:
    def __init__(self, inconsistencia, usuarios_anotaciones):
        self.inconsistencia = inconsistencia
        self.usuarios_anotaciones = usuarios_anotaciones


class PoliticaUsuarioGuardar:
    def __init__(self, politica_id, usuario_id, finalizado):
        self.politica_id = politica_id
        self.usuario_id = usuario_id
        self.finalizado = finalizado


class PoliticaAnotadorNoFinalizadas:
    def __init__(self, politica_id, politica_nombre, progreso):
        self.politica_id = politica_id
        self.politica_nombre = politica_nombre
        self.progreso = progreso


class PoliticaConsultarParrafos:
    def __init__(self, nombre, parrafos):
        self.nombre = nombre
        self.parrafos = parrafos

