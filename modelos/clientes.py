from pydantic import BaseModel

class ClienteBase(BaseModel):
    nombre: str
    edad: int
    correo: str
    descripcion: str | None = None

class ClienteCrear(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: int | None = None