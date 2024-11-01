import sqlalchemy as sa

from database.models import Base
import database.models as m


class ClientMatch(Base):
    __tablename__ = "client_match"

    client_id = sa.Column(sa.ForeignKey(m.Client.id, ondelete="CASCADE"))
    liked_client_id = sa.Column(sa.ForeignKey(m.Client.id, ondelete="CASCADE"))
    timestamp = sa.Column(sa.DateTime, server_default=sa.func.now())

    __table_args__ = (sa.PrimaryKeyConstraint(client_id, liked_client_id), )
