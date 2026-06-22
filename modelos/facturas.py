from pydantic import BaseModel, computed_field
from modelos.clientes import Cliente
from modelos.transacciones import Transaccion

class FacturaBase(BaseModel):
    cliente_id: int
    fecha: str

class FacturaCrear(FacturaBase):
    pass

class Factura(FacturaBase):
    id: int | None = None
    cliente: Cliente | None = None
    transacciones: list[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        """Calcula el valor total de la factura sumando todas las transacciones"""
        return sum(t.cantidad * t.vr_unitario for t in self.transacciones)