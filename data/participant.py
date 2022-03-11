import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Participants(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'participants'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=False)
    prize_id = sa.Column(sa.Integer, sa.ForeignKey("prizes.id"), nullable=True)
    prize = orm.relation('Prizes')
    promotion_id = sa.Column(sa.Integer, sa.ForeignKey("promotions.id"),
                             nullable=True)
    promotion = orm.relation('Promotions')
