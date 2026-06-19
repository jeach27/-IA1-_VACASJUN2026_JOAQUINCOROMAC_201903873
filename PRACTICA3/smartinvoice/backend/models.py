from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


class EstadoFactura(str, enum.Enum):
    PROCESADO = "Procesado"
    PENDIENTE = "Pendiente"
    ERROR = "Error"
    RECHAZADO = "Rechazado"


class RolUsuario(str, enum.Enum):
    ADMIN = "admin"
    USUARIO = "usuario"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(200), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(50), default=RolUsuario.USUARIO)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)

    facturas = relationship("Factura", back_populates="usuario")
    bitacoras = relationship("Bitacora", back_populates="usuario")
    reportes = relationship("Reporte", back_populates="usuario")


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nit = Column(String(20), unique=True, nullable=False)
    direccion = Column(String(300))
    email = Column(String(200))
    telefono = Column(String(30))
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    activo = Column(Boolean, default=True)

    facturas = relationship("Factura", back_populates="proveedor")


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    numero_factura = Column(String(50), index=True)
    fecha_factura = Column(String(20))
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    proveedor_nombre = Column(String(200))
    proveedor_nit = Column(String(20))
    subtotal = Column(Float, default=0.0)
    impuesto = Column(Float, default=0.0)
    total = Column(Float, default=0.0)
    archivo_nombre = Column(String(300))
    archivo_ruta = Column(String(500))
    estado = Column(String(20), default=EstadoFactura.PENDIENTE)
    fecha_carga = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    texto_extraido = Column(Text)
    errores_validacion = Column(Text)
    rpa_ejecutado = Column(Boolean, default=False)
    rpa_captura = Column(String(500))

    usuario = relationship("Usuario", back_populates="facturas")
    proveedor = relationship("Proveedor", back_populates="facturas")
    items = relationship("ItemFactura", back_populates="factura", cascade="all, delete-orphan")


class ItemFactura(Base):
    __tablename__ = "items_factura"

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    descripcion = Column(String(300))
    cantidad = Column(Float, default=1.0)
    precio_unitario = Column(Float, default=0.0)
    total = Column(Float, default=0.0)

    factura = relationship("Factura", back_populates="items")


class Bitacora(Base):
    __tablename__ = "bitacora"

    id = Column(Integer, primary_key=True, index=True)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    documento_nombre = Column(String(300))
    estado = Column(String(50))
    resultado = Column(String(500))
    detalles = Column(Text)

    usuario = relationship("Usuario", back_populates="bitacoras")


class Reporte(Base):
    __tablename__ = "reportes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(300), nullable=False)
    formato = Column(String(10), nullable=False)
    ruta_archivo = Column(String(500))
    fecha_generacion = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)

    usuario = relationship("Usuario", back_populates="reportes")
