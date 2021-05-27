from sources.connections import Base
from sqlalchemy import Column, String, DateTime, Integer, func, or_
from sqlalchemy.dialects.postgresql import JSONB


class CompanyModel(Base):
    __tablename__ = "company"

    # Primary key
    id = Column(Integer(), primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    locale_name = Column(JSONB(), nullable=False)

    # Auto Update Field
    create_datetime = Column(DateTime(timezone=True), index=True, default=func.now())
    update_datetime = Column(
        DateTime(timezone=True), index=True, default=func.now(), onupdate=func.now()
    )

    def __str__(self) -> str:
        return "{}, {}".format(self.id, self.locale_name)

    def response_body(self, locale) -> dict:
        locale_list = ["ko", "en", "jp"]
        available_name = self.locale_name.get(locale)
        if not available_name:
            for _ in locale_list:
                if self.locale_name.get(_):
                    available_name = self.locale_name.get(_)
                    break
        return {
            "company.id": self.id,
            "company.name": available_name,
            "company.locale_name": self.locale_name,
        }


if __name__ == "__main__":
    from sources.connections import session

    testing_data = session.query(CompanyModel).filter().offset(0).limit(3).all()
    for _ in testing_data:
        print("INPUT: ", _)

    query_data = (
        session.query(CompanyModel).filter(CompanyModel.name.contains("랩")).all()
    )
    for _ in query_data:
        print("RESULT", _)
