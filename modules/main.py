from flask import Flask, make_response
from flask_restful import Api, Resource
from semantic_search import SemanticSearch
from dimensionality_reduction import DimensionalityReduction
from fetch_data import FetchData
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)



# api.add_resource(MyResource, '/')

# Register API endpoints
api.add_resource(SemanticSearch, '/semantic_search')
api.add_resource(DimensionalityReduction, '/dimensionality_reduction')
api.add_resource(FetchData,'/fetch_data')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
