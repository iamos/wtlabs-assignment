from flask import request
from flask_restful import Resource

from sources.connections import session
from sources.models.company_model import CompanyModel


class CompanyRoute(Resource):
    """
    회사명 자동완성
        회사명의 일부만 들어가도 검색이 되어야 합니다.

    response examples;
        jobs?1621845827617
        &country=kr
        &job_sort=job.latest_order
        &company_tags=10022
        &locations=all
        &years=-1
    """

    def get(self):
        locale = request.args.get("locale")
        q = request.args.get("q")
        offset = request.args.get("offset", 0)
        limit = request.args.get("limit", 50)

        qr = (
            session.query(CompanyModel)
            .filter(CompanyModel.name.contains(q))
            .offset(offset)
            .limit(limit)
        )

        response_body = {"q": q, "locale": locale, "result": []}
        for _ in qr:
            response_body["result"].append(_.response_body(locale=locale))
        return response_body
