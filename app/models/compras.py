from app import db, cache


class Compras(db.Model):
    __tablename__ = "compras"
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer)
    fecha_compra = db.Column(db.DateTime)
    direccion_envio = db.Column(db.String(255))


    @staticmethod
    def crear_compra(producto_id, direccion_envio):
        nueva_compra = Compras(producto_id=producto_id, direccion_envio=direccion_envio)
        db.session.add(nueva_compra)
        db.session.commit()
        cache.set(f'compra_{nueva_compra.id}', nueva_compra, timeout=15)
        return nueva_compra

    @staticmethod
    def obtener_compras():
        result = cache.get("compras")
        if result is None:
            result = Compras.query.all()
            cache.set("compras", result, timeout=15)
        return result

    @staticmethod
    def obtener_compra_por_id(compra_id):
        return Compras.query.get(compra_id)