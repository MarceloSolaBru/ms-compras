from app.models.compras import Compras
import requests
import logging

class ComprasService:

    def procesar_pago(self, producto_id, monto, direccion_envio):
        url_pago = "http://localhost:5000/procesar_pago"
        datos_pago = {
            "producto_id": producto_id,
            "monto": monto,
            "direccion_envio": direccion_envio,
        }

        try:
            respuesta = requests.post(url_pago, json=datos_pago)

            if respuesta.status_code == 200:
                try:
                    return respuesta.json()  
                except ValueError:
                    logging.error("La respuesta no es un JSON válido")
                    return None
            else:
                logging.error(f"Error al procesar el pago: {respuesta.status_code} - {respuesta.text}")
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Error al conectar con el microservicio de pagos: {str(e)}")
            return None

    def guardar_compra(self, producto_id, direccion_envio):
        try:
            compra = Compras.crear_compra(producto_id, direccion_envio)
            return compra
        except Exception as e:
            logging.error(f"Error al guardar la compra: {str(e)}")
            return None

    def compra(self, producto_id, direccion_envio, monto):
        pago = self.procesar_pago(producto_id, monto, direccion_envio)
        if pago:
            return self.guardar_compra(producto_id, direccion_envio)
        else:
            logging.error("El pago no fue procesado correctamente.")
            return None
