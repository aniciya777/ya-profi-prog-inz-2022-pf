import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Prizes(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'prizes'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    description = sa.Column(sa.String, nullable=False)
    promotion_id = sa.Column(sa.Integer, sa.ForeignKey("promotions.id"),
                             nullable=True)
    promotion = orm.relation('Promotions')
