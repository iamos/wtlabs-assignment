from sources.connections import Base
from sqlalchemy import Column, Integer, JSON, DateTime, func, or_
from sqlalchemy.dialects.postgresql import JSONB


class TagModel(Base):
    __tablename__ = "tag"
    # Primary key
    id = Column(Integer(), primary_key=True, autoincrement=True)
    locale_tag = Column(JSONB(), nullable=False)

    # Auto Update Field
    create_datetime = Column(DateTime(timezone=True), index=True, default=func.now())
    update_datetime = Column(
        DateTime(timezone=True), index=True, default=func.now(), onupdate=func.now()
    )

    def to_json(self):
        return {
            "id": self.id,
            "locale_tag": self.locale_tag,
        }


if __name__ == "__main__":
    from sources.connections import session

    testing_data = session.query(TagModel).filter().offset(0).limit(3).all()
    for _ in testing_data:
        print(_.to_json())

    query_data = (
        session.query(TagModel)
        .filter(TagModel.locale_tag.contains({"en": "tag_4"}))
        .first()
    )
    print(query_data.locale_tag["jp"])
