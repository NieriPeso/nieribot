def estructura(id_remate, rematador, id_rem, remate_nombre, remate_descripcion, base, comienzo, final, img, activo=True, deletedAt=None, message_id=0, postores=[], legalAge=False):
    estructura = {
        'id': id_remate,
        'messageId': message_id,
        'ownerName': rematador,
        'ownerId': id_rem,
        'name': remate_nombre,
        'description': remate_descripcion,
        'baseAmount': base,
        'active': activo,
        'offers': postores,
        'image': img,
        'startAt': comienzo,
        'closeAt': final,
        'deletedAt': deletedAt,
        'legalAge': legalAge
    }
    return estructura

def extraer_datos(data):
    # ALL DATA : return data['_id'], data['id'], data['messageId'], data['ownerName'], data['ownerId'], data['name'], data['description'], data['baseAmount'], data['active'], data['offers'], data['image'], data['startedAt'], data['closeAt'], data['deletedAt']
    return data['_id'], data['id'], data['messageId'], data['ownerName'], data['ownerId'], data['name'], data['description'], data['baseAmount'], data['offers'], data['image'], data['startAt']
