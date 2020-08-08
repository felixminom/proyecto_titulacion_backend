def respuesta(exito, mensaje):
    estado = 'exito' if exito else 'fracaso'

    respuesta = {
        'estado': estado,
        'mensaje': mensaje
    }

    return respuesta
