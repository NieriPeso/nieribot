def estructura(id_remate, rematador, id_rem, remate_nombre, remate_descripcion, base, comienzo, final, img, activo=True, deletedAt=None, message_id=0, postores=[]):
    estructura = {
        'ID': id_remate,
        'message_id': message_id,
        'rematador': rematador,
        'id_rematador': id_rem,
        'nombre_rem': remate_nombre,
        'descripcion_rem': remate_descripcion,
        'base': base,
        'comienzo': comienzo,
        'activo': activo,
        'cierre': final.replace('\n', ''),
        'postores': postores,
        'foto': img,
        'deletedAt': deletedAt
    }
    return estructura

def extraer_datos(data):
    return data['_id'], data['ID'], data['message_id'], data['rematador'], data['id_rematador'], data['nombre_rem'], data['descripcion_rem'], data['base'], data['comienzo'], data['activo'], data['postores'], data['foto']
