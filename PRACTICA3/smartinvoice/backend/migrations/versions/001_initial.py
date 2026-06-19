"""Initial migration - create all tables

Revision ID: 001
Revises:
Create Date: 2026-06-19

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(100), nullable=False),
        sa.Column("email", sa.String(200), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("rol", sa.String(50), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_usuarios_id", "usuarios", ["id"])
    op.create_index("ix_usuarios_username", "usuarios", ["username"], unique=True)
    op.create_index("ix_usuarios_email", "usuarios", ["email"], unique=True)

    op.create_table(
        "proveedores",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(200), nullable=False),
        sa.Column("nit", sa.String(20), nullable=False),
        sa.Column("direccion", sa.String(300), nullable=True),
        sa.Column("email", sa.String(200), nullable=True),
        sa.Column("telefono", sa.String(30), nullable=True),
        sa.Column("fecha_creacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nit"),
    )
    op.create_index("ix_proveedores_id", "proveedores", ["id"])

    op.create_table(
        "facturas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero_factura", sa.String(50), nullable=True),
        sa.Column("fecha_factura", sa.String(20), nullable=True),
        sa.Column("proveedor_id", sa.Integer(), nullable=True),
        sa.Column("proveedor_nombre", sa.String(200), nullable=True),
        sa.Column("proveedor_nit", sa.String(20), nullable=True),
        sa.Column("subtotal", sa.Float(), nullable=True),
        sa.Column("impuesto", sa.Float(), nullable=True),
        sa.Column("total", sa.Float(), nullable=True),
        sa.Column("archivo_nombre", sa.String(300), nullable=True),
        sa.Column("archivo_ruta", sa.String(500), nullable=True),
        sa.Column("estado", sa.String(20), nullable=True),
        sa.Column("fecha_carga", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("texto_extraido", sa.Text(), nullable=True),
        sa.Column("errores_validacion", sa.Text(), nullable=True),
        sa.Column("rpa_ejecutado", sa.Boolean(), nullable=True),
        sa.Column("rpa_captura", sa.String(500), nullable=True),
        sa.ForeignKeyConstraint(["proveedor_id"], ["proveedores.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_facturas_id", "facturas", ["id"])
    op.create_index("ix_facturas_numero_factura", "facturas", ["numero_factura"])

    op.create_table(
        "items_factura",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("factura_id", sa.Integer(), nullable=False),
        sa.Column("descripcion", sa.String(300), nullable=True),
        sa.Column("cantidad", sa.Float(), nullable=True),
        sa.Column("precio_unitario", sa.Float(), nullable=True),
        sa.Column("total", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["factura_id"], ["facturas.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_items_factura_id", "items_factura", ["id"])

    op.create_table(
        "bitacora",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fecha_hora", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.Column("documento_nombre", sa.String(300), nullable=True),
        sa.Column("estado", sa.String(50), nullable=True),
        sa.Column("resultado", sa.String(500), nullable=True),
        sa.Column("detalles", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_bitacora_id", "bitacora", ["id"])

    op.create_table(
        "reportes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(300), nullable=False),
        sa.Column("formato", sa.String(10), nullable=False),
        sa.Column("ruta_archivo", sa.String(500), nullable=True),
        sa.Column("fecha_generacion", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("usuario_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuarios.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reportes_id", "reportes", ["id"])


def downgrade() -> None:
    op.drop_table("reportes")
    op.drop_table("bitacora")
    op.drop_table("items_factura")
    op.drop_table("facturas")
    op.drop_table("proveedores")
    op.drop_table("usuarios")
