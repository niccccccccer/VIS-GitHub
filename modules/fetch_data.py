from flask_restful import Resource
import json
from flask import request

class FetchData(Resource):
    def post(self):
        data = request.get_json()
        # type=data['type']
        owner = data['owner']
        repo = data['repo']
        # dic={'star':'stars','fork':'forks','pull':'pulls','commit':'commits'}
        # type=dic[type]

        print(f'../assets/data/{owner}_{repo}.json')
        with open(f'../assets/data/{owner}_{repo}.json', "r") as f:
            data = json.load(f)
        return data