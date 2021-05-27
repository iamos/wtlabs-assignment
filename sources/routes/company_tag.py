from flask import request
from flask_restful import Resource, abort

from sources.connections import session
from sources.models.company_model import CompanyModel
from sources.models.company_tag_model import CompanyTagModel
from sources.models.tag_model import TagModel


class CompanyTagRoute(Resource):
    def get(self):
        # Debugging용 API
        company_id = request.args.get("company_id", None)
        if not company_id:
            abort(400)

        q_generator = (
            session.query(CompanyTagModel)
            .filter(CompanyTagModel.company_id == company_id)
            .order_by(CompanyTagModel.tag_id)
        )

        response_body = {"company_id": company_id, "result": []}
        for _ in q_generator:
            response_body["result"].append(_.tag_id)
        return response_body

    def put(self):
        # 회사 태그 정보 추가
        company_id = request.get_json().get("company_id", None)
        tag_ids = request.get_json().get("tag_id", [])

        for tid in tag_ids:
            CompanyTagModel.add_tag(session=session, company_id=company_id, tag_id=tid)
        try:
            session.commit()
        except Exception:
            session.rollback()
            abort(500)

    def delete(self):
        """
        회사 태그 정보 삭제
        """
        company_id = request.get_json().get("company_id", None)
        tag_id = request.get_json().get("tag_id")

        qr = (
            session.query(CompanyTagModel)
            .filter(
                CompanyTagModel.company_id == company_id,
                CompanyTagModel.tag_id == tag_id,
            )
            .first()
        )
        if not qr:
            abort(404)

        session.delete(qr)
        try:
            session.commit()
        except Exception:
            abort(500)
        return 204
