from sqlalchemy.sql.schema import ForeignKeyConstraint, UniqueConstraint
from sources.connections import Base
from sqlalchemy import Column, Integer, func, or_


class CompanyTagModel(Base):
    __tablename__ = "company_tag"
    __table_args__ = (
        ForeignKeyConstraint(["company_id"], ["company.id"]),
        ForeignKeyConstraint(["tag_id"], ["tag.id"]),
        UniqueConstraint("company_id", "tag_id"),
    )

    # Primary key
    id = Column(Integer(), primary_key=True, autoincrement=True)

    company_id = Column(Integer(), nullable=False)
    tag_id = Column(Integer(), nullable=False)

    def __str__(self):
        return "{}, {}".format(self.company_id, self.tag_id)

    @classmethod
    def add_tag(cls, session, company_id, tag_id) -> bool:
        # 회사에 해당 태그가 없을때만 추가
        print(
            session.query(cls)
            .filter(
                cls.company_id == company_id,
                cls.tag_id == tag_id,
            )
            .first()
        )
        if (
            not session.query(cls)
            .filter(
                cls.company_id == company_id,
                cls.tag_id == tag_id,
            )
            .first()
        ):
            session.add(cls(company_id=company_id, tag_id=tag_id))
            return True
        return False


if __name__ == "__main__":
    from sources.connections import session
    from sources.models.tag_model import TagModel
    from sources.models.company_model import CompanyModel

    qr = (
        session.query(CompanyModel)
        .filter(
            CompanyModel.id == CompanyTagModel.company_id,
            TagModel.id == CompanyTagModel.tag_id,
            TagModel.locale_tag.contains({"jp": "タグ_4"}),
        )
        .all()
    )
    for _ in qr:
        print(_)
