from app.models.compras import Compras
import requests
import logging

class ComprasService:

    def procesar_pago(self, producto_id, direccion_envio):
        url_pago = "http://localhost:5000/procesar_pago"  # Considera mover esto a una configuración
        datos_pago = {
            "producto_id": producto_id,
            "direccion_envio": direccion_envio,
        }

        try:
            respuesta = requests.post(url_pago, json=datos_pago)

            if respuesta.status_code == 200:
                return respuesta.json()
            else:
                logging.error(f"Error al procesar el pago: {respuesta.status_code} - {respuesta.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al conectar con el microservicio de pagos: {str(e)}")
            return None

    def guardar_compra(self, producto_id, direccion_envio):
        try:
            return Compras.crear_compra(producto_id, direccion_envio)
        except Exception as e:
            logging.error(f"Error al guardar la compra: {str(e)}")
            return None

    def compra(self, producto_id, direccion_envio):
        # Validaciones
        if not isinstance(producto_id, int) or not isinstance(direccion_envio, str):
            logging.error("Datos inválidos para el pago")
            return None

        pago = self.procesar_pago(producto_id, direccion_envio)
        if pago:
            return self.guardar_compra(producto_id, direccion_envio)
        else:
            logging.error("El pago no fue procesado correctamente.")
            return None
