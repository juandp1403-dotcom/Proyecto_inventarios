from app import create_app, db
from app.models.ambiente import Ambiente
from app.models.articulo import Articulo
from app.models.inventario import Inventario

def update_inventario_208():
    app = create_app()
    with app.app_context():
        # Obtener ambiente 208
        ambiente = Ambiente.query.filter_by(nombre='Ambiente 208').first()
        if not ambiente:
            print("Ambiente 208 no encontrado")
            return
        
        print(f"Ambiente 208 encontrado con ID: {ambiente.id}")
        
        # Actualizar cantidades en el inventario
        inventario_updates = {
            'Silla': 10,
            'Computador': 10,  # Actualizado a 10
            'Mesa': 10,
            'TV': 1
        }
        
        for articulo_nombre, nueva_cantidad in inventario_updates.items():
            # Buscar el artículo
            articulo = Articulo.query.filter_by(nombre=articulo_nombre).first()
            if not articulo:
                print(f"Artículo {articulo_nombre} no encontrado")
                continue
                
            # Buscar el inventario para este ambiente y artículo
            inventario = Inventario.query.filter_by(
                id_ambiente=ambiente.id,
                id_articulo=articulo.id
            ).first()
            
            if inventario:
                # Actualizar cantidad existente
                print(f"Actualizando {articulo_nombre}: {inventario.cantidad} -> {nueva_cantidad}")
                inventario.cantidad = nueva_cantidad
            else:
                # Crear nuevo registro de inventario
                print(f"Creando {articulo_nombre} con cantidad {nueva_cantidad}")
                inventario = Inventario(
                    id_ambiente=ambiente.id,
                    id_articulo=articulo.id,
                    cantidad=nueva_cantidad,
                    cantidad_minima=2
                )
                db.session.add(inventario)
        
        # Guardar cambios
        db.session.commit()
        print("Inventario del ambiente 208 actualizado exitosamente")
        
        # Mostrar inventario actual
        print("\nInventario actual del ambiente 208:")
        inventario_actual = Inventario.query.filter_by(id_ambiente=ambiente.id).all()
        for inv in inventario_actual:
            articulo = Articulo.query.get(inv.id_articulo)
            print(f"- {articulo.nombre}: {inv.cantidad} unidades")

if __name__ == '__main__':
    update_inventario_208()
