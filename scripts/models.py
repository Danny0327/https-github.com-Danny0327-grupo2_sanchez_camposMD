from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Text
from sqlalchemy import String

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class APOD(Base):

    __tablename__ = "apod"

    date = Column(
        Date,
        primary_key=True
    )

    title = Column(
        Text,
        nullable=False
    )

    media_type = Column(
        String(50),
        nullable=True
    )

    url = Column(
        Text,
        nullable=True
    )

    explanation = Column(
        Text,
        nullable=True
    )

    copyright = Column(
        Text,
        nullable=True
    )

    def __repr__(self):

        return (
            f"<APOD(date={self.date}, "
            f"title={self.title})>"
        )