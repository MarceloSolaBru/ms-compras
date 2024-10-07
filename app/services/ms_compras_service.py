from app.models.compras import Compras
import requests

class Compras_service ():
    def procesar_pago_y_guardar_compra(producto_id, direccion_envio, monto):
        # URL del microservicio de pagos
        url_pago = "http://localhost:5000/procesar_pago"  # Cambia el puerto según corresponda
    
        # Datos para el pago
        datos_pago = {
            "producto_id": producto_id,
            "monto": monto,
            "direccion_envio": direccion_envio,
        }
        try:
            # Hacer la solicitud al microservicio de pagos
            respuesta = requests.post(url_pago, json=datos_pago)
        
            # Verificar si el pago fue exitoso
            if respuesta.status_code == 200:
                # Si el pago fue exitoso, guardar la compra
                compra = Compras.crear_compra(producto_id, direccion_envio)
                return compra
            else:
                # Manejar error de pago
                print("Error al procesar el pago:", respuesta.json())
                return None
            
        except requests.exceptions.RequestException as e:
            # Manejar errores de conexión
            print("Error al conectar con el microservicio de pagos:", str(e))
            return None
