from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear
from modelos.facturas import Factura, FacturaCrear
from modelos.transacciones import Transaccion, TransaccionCrear

app = FastAPI(title="API de Gestión", description="API para gestionar clientes, facturas y transacciones")

# ============= BASES DE DATOS SIMULADAS =============
lista_clientes: list[Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transaccion] = []

# ============= ENDPOINT DE INICIO =============
@app.get("/")
def inicio():
    return {"mensaje": "Aprendiendo fastapi"}

# ======================================================
# ============= ENDPOINTS PARA CLIENTES =============
# ======================================================

@app.get("/clientes", response_model=list[Cliente])
def listar_clientes():
    """Lista todos los clientes"""
    return lista_clientes

@app.get("/clientes/{id}", response_model=Cliente)
def obtener_cliente(id: int):
    """Obtiene un cliente por su ID"""
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente
    raise HTTPException(status_code=404, detail=f"Cliente con id {id} no encontrado")

@app.post("/clientes", response_model=Cliente)
def crear_cliente(datos_cliente: ClienteCrear):
    """Crea un nuevo cliente"""
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes) + 1
    lista_clientes.append(cliente_val)
    return cliente_val

@app.put("/clientes/{id}", response_model=Cliente)
def editar_cliente(id: int, datos_cliente: Cliente):
    """Edita un cliente existente"""
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val
            return cliente_val
    raise HTTPException(status_code=404, detail=f"Cliente con id {id} no encontrado")

@app.delete("/clientes/{id}")
def eliminar_cliente(id: int):
    """Elimina un cliente por su ID"""
    for i, cliente in enumerate(lista_clientes):
        if cliente.id == id:
            lista_clientes.pop(i)
            return {"mensaje": f"Cliente {id} eliminado correctamente"}
    raise HTTPException(status_code=404, detail=f"Cliente con id {id} no encontrado")

# ======================================================
# ============= ENDPOINTS PARA FACTURAS =============
# ======================================================

@app.get("/facturas", response_model=list[Factura])
def listar_facturas():
    """Lista todas las facturas"""
    return lista_facturas

@app.get("/facturas/{id}", response_model=Factura)
def obtener_factura(id: int):
    """Obtiene una factura por su ID"""
    for factura in lista_facturas:
        if factura.id == id:
            return factura
    raise HTTPException(status_code=404, detail=f"Factura con id {id} no encontrada")

@app.post("/facturas", response_model=Factura)
def crear_factura(datos_factura: FacturaCrear):
    """Crea una nueva factura (requiere cliente existente)"""
    # Verificar que el cliente existe
    cliente_obj = None
    for cliente in lista_clientes:
        if cliente.id == datos_factura.cliente_id:
            cliente_obj = cliente
            break
    
    if not cliente_obj:
        raise HTTPException(status_code=404, detail=f"Cliente con id {datos_factura.cliente_id} no encontrado")
    
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.cliente = cliente_obj
    lista_facturas.append(factura_val)
    return factura_val

@app.put("/facturas/{id}", response_model=Factura)
def editar_factura(id: int, datos_factura: FacturaCrear):
    """Edita una factura existente"""
    for i, factura in enumerate(lista_facturas):
        if factura.id == id:
            # Verificar que el cliente existe
            cliente_obj = None
            for cliente in lista_clientes:
                if cliente.id == datos_factura.cliente_id:
                    cliente_obj = cliente
                    break
            
            if not cliente_obj:
                raise HTTPException(status_code=404, detail=f"Cliente con id {datos_factura.cliente_id} no encontrado")
            
            factura_actualizada = Factura.model_validate(datos_factura.model_dump())
            factura_actualizada.id = id
            factura_actualizada.cliente = cliente_obj
            factura_actualizada.transacciones = factura.transacciones  # Mantener transacciones existentes
            lista_facturas[i] = factura_actualizada
            return factura_actualizada
    raise HTTPException(status_code=404, detail=f"Factura con id {id} no encontrada")

@app.delete("/facturas/{id}")
def eliminar_factura(id: int):
    """Elimina una factura por su ID"""
    for i, factura in enumerate(lista_facturas):
        if factura.id == id:
            lista_facturas.pop(i)
            return {"mensaje": f"Factura {id} eliminada correctamente"}
    raise HTTPException(status_code=404, detail=f"Factura con id {id} no encontrada")

# ======================================================
# ============= ENDPOINTS PARA TRANSACCIONES =============
# ======================================================

@app.get("/transacciones", response_model=list[Transaccion])
def listar_transacciones():
    """Lista todas las transacciones"""
    return lista_transacciones

@app.get("/transacciones/{id}", response_model=Transaccion)
def obtener_transaccion(id: int):
    """Obtiene una transacción por su ID"""
    for transaccion in lista_transacciones:
        if transaccion.id == id:
            return transaccion
    raise HTTPException(status_code=404, detail=f"Transacción con id {id} no encontrada")

@app.post("/transacciones", response_model=Transaccion)
def crear_transaccion(datos_transaccion: TransaccionCrear):
    """Crea una nueva transacción (requiere factura existente)"""
    # Verificar que la factura existe
    factura_obj = None
    for factura in lista_facturas:
        if factura.id == datos_transaccion.factura_id:
            factura_obj = factura
            break
    
    if not factura_obj:
        raise HTTPException(status_code=404, detail=f"Factura con id {datos_transaccion.factura_id} no encontrada")
    
    transaccion_val = Transaccion.model_validate(datos_transaccion.model_dump())
    transaccion_val.id = len(lista_transacciones) + 1
    lista_transacciones.append(transaccion_val)
    
    # Agregar la transacción a la factura
    factura_obj.transacciones.append(transaccion_val)
    
    return transaccion_val

@app.put("/transacciones/{id}", response_model=Transaccion)
def editar_transaccion(id: int, datos_transaccion: TransaccionCrear):
    """Edita una transacción existente"""
    for i, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            # Verificar que la factura existe
            factura_obj = None
            for factura in lista_facturas:
                if factura.id == datos_transaccion.factura_id:
                    factura_obj = factura
                    break
            
            if not factura_obj:
                raise HTTPException(status_code=404, detail=f"Factura con id {datos_transaccion.factura_id} no encontrada")
            
            # Actualizar transacción
            transaccion_actualizada = Transaccion.model_validate(datos_transaccion.model_dump())
            transaccion_actualizada.id = id
            lista_transacciones[i] = transaccion_actualizada
            
            # Actualizar en la factura también
            for factura in lista_facturas:
                for j, trans in enumerate(factura.transacciones):
                    if trans.id == id:
                        factura.transacciones[j] = transaccion_actualizada
                        break
            
            return transaccion_actualizada
    raise HTTPException(status_code=404, detail=f"Transacción con id {id} no encontrada")

@app.delete("/transacciones/{id}")
def eliminar_transaccion(id: int):
    """Elimina una transacción por su ID"""
    for i, transaccion in enumerate(lista_transacciones):
        if transaccion.id == id:
            # Eliminar de la factura también
            for factura in lista_facturas:
                factura.transacciones = [t for t in factura.transacciones if t.id != id]
            
            lista_transacciones.pop(i)
            return {"mensaje": f"Transacción {id} eliminada correctamente"}
    raise HTTPException(status_code=404, detail=f"Transacción con id {id} no encontrada")