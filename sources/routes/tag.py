from flask import request
from flask_restful import Resource

from sources.connections import session
from sources.models.company_model import CompanyModel
from sources.models.company_tag_model import CompanyTagModel
from sources.models.tag_model import TagModel

"""
태그명으로 회사 검색
    태그로 검색 관련된 회사가 검색되어야 합니다.
    다국어로 검색이 가능해야 합니다.
    일본어 태그로 검색을 해도 한국 회사가 노출이 되어야 합니다.
    タグ_4로 검색 했을 때, 원티드랩 회사 정보가 노출이 되어야 합니다.
    동일한 회사는 한번만 노출이 되어야합니다.
"""


class TagRoute(Resource):
    def get(self):
        # /tag?q=<string>&locale=<string>
        locale = request.args.get("locale")
        q = request.args.get("q")
        offset = request.args.get("offset", 0)
        limit = request.args.get("limit", 50)

        qr = (
            session.query(CompanyModel)
            .filter(
                CompanyModel.id == CompanyTagModel.company_id,
                TagModel.id == CompanyTagModel.tag_id,
                TagModel.locale_tag.contains({locale: q}),
            )
            .offset(offset)
            .limit(limit)
        )

        response_body = {"q": q, "locale": locale, "result": []}
        for _ in qr:
            response_body["result"].append(_.response_body(locale=locale))
        return response_body
