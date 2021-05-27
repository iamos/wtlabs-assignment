from flask import Flask
from flask_restful import Api

from sources.routes.healthcheck import Healthcheck
from sources.routes.company import CompanyRoute
from sources.routes.tag import TagRoute
from sources.routes.company_tag import CompanyTagRoute


def start_app():
    from sources.init_database import init_db_from_tempfile

    init_db_from_tempfile()
    return Flask(__name__)


app = start_app()
api = Api(app)

api.add_resource(Healthcheck, "/healthcheck")
api.add_resource(CompanyRoute, "/company")
api.add_resource(TagRoute, "/tag")
api.add_resource(CompanyTagRoute, "/companytag")


if __name__ == "__main__":
    app.run(debug=True)
