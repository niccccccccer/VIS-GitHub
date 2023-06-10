from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport
import argparse
import json
from tqdm import tqdm
import os
current_path=os.path.dirname(__file__)
# read token
token_path = current_path+'/token.txt'
with open(token_path, "r", encoding='utf-8') as infile:
    token = infile.read()
# token='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'
header = {
    'Authorization': f'Bearer {token}'
}
parser = argparse.ArgumentParser()
parser.add_argument("--owner", type=str, default='modelmapper') # scikit-learn
parser.add_argument("--repo", type=str, default='modelmapper')
args = parser.parse_args()
owner = args.owner
repo = args.repo
index=0
# use GitHub graphql API
transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=header)
client = Client(transport=transport, fetch_schema_from_transport=True)


query_basic = gql(
    """
    query ($owner: String!, $repo: String!) {
        repository(owner: $owner, name: $repo) {
        description
        homepageUrl
        forkCount
        stargazerCount
        }
    }
    """
)

params = {"owner": owner, "repo": repo}
result={}
try:
    result = client.execute(query_basic, variable_values=params)['repository']
except Exception as e:
    print(e)
    print('Retrying...')
    
# save the result into json file
with open(f'./{owner}_{repo}_description.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(result))