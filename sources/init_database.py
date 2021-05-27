from sources.connections import Base, _ENGINE, session
from sources.import_csv import WantedCSVReader


def create_tables():
    from sources.models.company_model import CompanyModel
    from sources.models.tag_model import TagModel
    from sources.models.company_tag_model import CompanyTagModel

    Base.metadata.create_all(bind=_ENGINE)


def init_company():
    from sources.models.company_model import CompanyModel

    if (
        not session.query(CompanyModel)
        .filter(CompanyModel.name.contains("원티드랩"))
        .first()
    ):
        session.add(
            CompanyModel(
                name="원티드랩, Wantedlab", locale_name={"ko": "원티드랩", "en": "Wantedlab"}
            )
        )
        session.commit()
        print("\tADD Company('원티드랩')")

    if not session.query(CompanyModel).filter(CompanyModel.name.contains("원트")).first():
        session.add(
            CompanyModel(name="원트, Want", locale_name={"ko": "원트", "en": "Want"})
        )
        session.commit()
        print("\tADD Company('원트')")


def init_tag():
    from sources.models.tag_model import TagModel

    if not session.query(TagModel).filter(TagModel.id == 4).first():
        session.add(
            TagModel(id=4, locale_tag={"ko": "태그_4", "en": "tag_4", "jp": "タグ_4"})
        )
        session.commit()
        print("\tADD Tag(4)")
    if not session.query(TagModel).filter(TagModel.id == 16).first():
        session.add(
            TagModel(id=16, locale_tag={"ko": "태그_16", "en": "tag_16", "jp": "タグ_16"})
        )
        session.commit()
        print("\tADD Tag(16)")
    if not session.query(TagModel).filter(TagModel.id == 20).first():
        session.add(
            TagModel(id=20, locale_tag={"ko": "태그_20", "en": "tag_20", "jp": "タグ_20"})
        )
        session.commit()
        print("\tADD Tag(20)")


def init_company_tag():
    from sources.models.company_tag_model import CompanyTagModel

    if (
        not session.query(CompanyTagModel)
        .filter(CompanyTagModel.company_id == 1, CompanyTagModel.tag_id == 4)
        .first()
    ):
        session.add(CompanyTagModel(company_id=1, tag_id=4))
        session.commit()
        print("\tADD CompanyTag(1,4)")

    if (
        not session.query(CompanyTagModel)
        .filter(CompanyTagModel.company_id == 2, CompanyTagModel.tag_id == 4)
        .first()
    ):
        session.add(CompanyTagModel(company_id=2, tag_id=4))
        session.commit()
        print("\tADD CompanyTag(2,4)")

    if (
        not session.query(CompanyTagModel)
        .filter(CompanyTagModel.company_id == 1, CompanyTagModel.tag_id == 16)
        .first()
    ):
        session.add(CompanyTagModel(company_id=1, tag_id=16))
        session.commit()
        print("\tADD CompanyTag(1,16)")


def init_database():
    print("init_database()")
    create_tables()
    init_company()
    init_tag()
    init_company_tag()


def init_csv():
    from sources.models.company_model import CompanyModel
    from sources.models.tag_model import TagModel
    from sources.models.company_tag_model import CompanyTagModel

    for _ in range(1, 31):
        if not session.query(TagModel).filter(TagModel.id == _).first():
            session.add(
                TagModel(
                    id=_,
                    locale_tag={
                        "ko": "태그_{}".format(_),
                        "en": "tag_{}".format(_),
                        "jp": "タグ_{}".format(_),
                    },
                )
            )
            print("\t ADD Tag({})".format(_))
            session.flush()
    session.commit()

    wcr = WantedCSVReader()
    for _ in wcr.readline():
        if not session.query(CompanyModel).filter(CompanyModel.name == _[0]).first():
            company_model = CompanyModel(name=_[0], locale_name=_[1])
            session.add(company_model)
            session.flush()
            company_id = company_model.id
            for tid in _[2]:
                if (
                    not session.query(CompanyTagModel)
                    .filter(
                        CompanyTagModel.company_id == company_id,
                        CompanyTagModel.tag_id == tid[3:],
                    )
                    .first()
                ):
                    session.add(CompanyTagModel(company_id=company_id, tag_id=tid[3:]))
            print("\t ADD Company({})".format(_))
        session.commit()


def init_db_from_tempfile():
    create_tables()
    init_csv()


if __name__ == "__main__":
    init_db_from_tempfile()
