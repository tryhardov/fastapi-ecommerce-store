import uuid

from sqlalchemy import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDPrimaryKeyMixin


class CartItem(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = 'cart_items'
    __table_args__ = (
        CheckConstraint('quantity > 0', name='quantity_positive'),
        UniqueConstraint('cart_id', 'product_id', name='uq_cart_items_cart_id_product_id'),
        )

    cart_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('carts.id', ondelete='CASCADE',))
    product_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('products.id', ondelete='CASCADE'))
    quantity: Mapped[int] 