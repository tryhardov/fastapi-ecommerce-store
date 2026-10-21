import uuid
from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Numeric, String, Text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class Product(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = 'products'
    __table_args__ = (
        CheckConstraint('price >= 0', name='price_non_negative'),
        CheckConstraint('stock >= 0', name='stock_non_negative'),
    )

    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('categories.id', ondelete='RESTRICT'), index=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    stock: Mapped[int] = mapped_column(server_default='0')
    description: Mapped[str | None] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(server_default=true())

    category: Mapped['Category'] = relationship()