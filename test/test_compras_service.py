import unittest
from unittest.mock import patch, MagicMock
import requests
from app.services.compras_service import ComprasService
from app.models.compras import Compras

class TestComprasService(unittest.TestCase):
    def setUp(self):
        self.compras_service = ComprasService()

    @patch('app.services.compras_service.requests.post')
    def test_procesar_pago_exitoso(self, mock_post):
        mock_respuesta = MagicMock()
        mock_respuesta.status_code = 200
        mock_respuesta.json.return_value = {"status": "success"}
        mock_post.return_value = mock_respuesta

        resultado = self.compras_service.procesar_pago(1, "Calle Falsa 123")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado["status"], "success")

    @patch('app.services.compras_service.requests.post')
    def test_procesar_pago_fallo(self, mock_post):
        mock_respuesta = MagicMock()
        mock_respuesta.status_code = 400
        mock_respuesta.text = "Error al procesar el pago"
        mock_post.return_value = mock_respuesta

        resultado = self.compras_service.procesar_pago(1, "Calle Falsa 123")

        self.assertIsNone(resultado)

    @patch('app.services.compras_service.requests.post')
    def test_procesar_pago_error_conexion(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Error de conexión")

        resultado = self.compras_service.procesar_pago(1, "Calle Falsa 123")

        self.assertIsNone(resultado)

    @patch.object(Compras, 'crear_compra')
    def test_guardar_compra_exitoso(self, mock_crear_compra):
        mock_compra = Compras(producto_id=1, direccion_envio="Calle Falsa 123")
        mock_crear_compra.return_value = mock_compra

        resultado = self.compras_service.guardar_compra(1, "Calle Falsa 123")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.producto_id, 1)
        self.assertEqual(resultado.direccion_envio, "Calle Falsa 123")

    @patch.object(Compras, 'crear_compra')
    def test_guardar_compra_error(self, mock_crear_compra):
        mock_crear_compra.side_effect = Exception("Error al guardar la compra")

        resultado = self.compras_service.guardar_compra(1, "Calle Falsa 123")

        self.assertIsNone(resultado)

    @patch('app.services.compras_service.requests.post')
    @patch.object(Compras, 'crear_compra')
    def test_compra_exitoso(self, mock_crear_compra, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "success"}

        mock_compra = Compras(producto_id=1, direccion_envio="Calle Falsa 123")
        mock_crear_compra.return_value = mock_compra

        resultado = self.compras_service.compra(1, "Calle Falsa 123")

        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.producto_id, 1)
        self.assertEqual(resultado.direccion_envio, "Calle Falsa 123")

    @patch('app.services.compras_service.requests.post')
    def test_compra_fallo_pago(self, mock_post):
        mock_post.return_value.status_code = 400

        resultado = self.compras_service.compra(1, "Calle Falsa 123")

        self.assertIsNone(resultado)

    @patch('app.services.compras_service.requests.post')
    def test_compra_error_conexion(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException("Error de conexión")

        resultado = self.compras_service.compra(1, "Calle Falsa 123")

        self.assertIsNone(resultado)

if __name__ == "__main__":
    unittest.main()
