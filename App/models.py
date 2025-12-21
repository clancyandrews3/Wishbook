########################################
# This file is designed to add backend functionality
# to the website via database setup and management
#
#
########################################

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from App import login, db


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    firstname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    lastname: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(128), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}'

class Item(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    url: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    image_url: so.Mapped[str] = so.mapped_column(sa.String(256), index=True)
    price: so.Mapped[float] = so.mapped_column(index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Item {self.name}'

class Wishlists(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    is_public: so.Mapped[bool] = so.mapped_column(sa.Boolean, index=True)
    created_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Wishlist {self.name}'

class WishlistItem(db.Model):
    wishlist_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Wishlists.id), primary_key=True)
    item_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Item.id), primary_key=True)
    priority: so.Mapped[int] = so.mapped_column(index=True)
    quantity: so.Mapped[int] = so.mapped_column(index=True, default=1)
    notes: so.Mapped[str] = so.mapped_column(sa.String(256))
    added_at: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Wishlist Item {self.notes}'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))