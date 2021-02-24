from flasgger import swag_from
from flask import request, Response, current_app

from app.doc.account.signup import SIGNUP_POST
from app.model import UnsignedStudentModel, StudentModel, PointStatusModel, StayApplyModel
from app.util.json_schema import json_type_validate, SIGNUP_POST_JSON
from app.view.base_resource import AccountResource


class Signup(AccountResource):
    @json_type_validate(SIGNUP_POST_JSON)
    @swag_from(SIGNUP_POST)
    def post(self):
        id = request.json['id']
        pw = request.json['password']
        name = request.json['name']
        number = request.json['number']

        if not request.json['key'] == current_app.config["SIGNUP_KEY"]:
            return Response('', 401)

        StudentModel.signup(id, pw, name, number)
        PointStatusModel(id).save()
        StayApplyModel(id, 4).save()

        return Response('', 201)
