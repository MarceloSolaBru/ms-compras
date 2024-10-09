from flask import Blueprint, jsonify, request
from app.models.compras import Compras
from app import db
from datetime import datetime

# Definir el Blueprint para compras
compras_bp = Blueprint('compras', __name__)

@compras_bp.route('/', methods=['POST'])
def create_compra():
    data = request.get_json()
    
    if not data or not 'producto_id' in data or not 'direccion_envio' in data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    # Procesar compra
    compra = Compras.crear_compra(data['producto_id'], data['direccion_envio'])
    
    if compra is None:
        return jsonify({'error': 'Error al procesar la compra'}), 500
    
    return jsonify({'id': compra.id, 'producto_id': compra.producto_id, 'direccion_envio': compra.direccion_envio}), 201

@compras_bp.route('/<int:id>', methods=['GET'])
def get_compra(id):
    compra = Compras.obtener_compra_por_id(id)
    if compra is None:
        return jsonify({'error': 'Compra no encontrada'}), 404
    return jsonify({'id': compra.id, 'producto_id': compra.producto_id, 'direccion_envio': compra.direccion_envio})

@compras_bp.route('/', methods=['GET'])
def get_compras():
    compras = Compras.obtener_compras()
    return jsonify([{'id': compra.id, 'producto_id': compra.producto_id, 'direccion_envio': compra.direccion_envio} for compra in compras])

@compras_bp.route('/<int:id>', methods=['PUT'])
def update_compra(id):
    compra = Compras.obtener_compra_por_id(id)
    if compra is None:
        return jsonify({'error': 'Compra no encontrada'}), 404

    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    compra.producto_id = data.get('producto_id', compra.producto_id)
    compra.direccion_envio = data.get('direccion_envio', compra.direccion_envio)
    db.session.commit()
    
    return jsonify({'id': compra.id, 'producto_id': compra.producto_id, 'direccion_envio': compra.direccion_envio})

@compras_bp.route('/<int:id>', methods=['DELETE'])
def delete_compra(id):
    compra = Compras.obtener_compra_por_id(id)
    if compra is None:
        return jsonify({'error': 'Compra no encontrada'}), 404
    
    db.session.delete(compra)
    db.session.commit()
    return jsonify({'message': 'Compra eliminada'}), 200
