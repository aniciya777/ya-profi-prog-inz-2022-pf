import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Promotions(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'promotions'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    prizes = orm.relation("Prizes", back_populates='promotion')
    participants = orm.relation("Participants", back_populates='promotion')
