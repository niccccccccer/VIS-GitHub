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

# fetch all pull requests
query = gql(
    """
    query ($owner: String!, $repo: String!, $after: String, $after_files: String) {
        repository(owner: $owner, name: $repo) {
        description
        homepageUrl
            pullRequests(first: 10, after: $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                nodes {
                    number
                    title
                    body
                    url

                    additions
                    deletions
                    files(first: 40, after: $after_files) {
                        pageInfo {
                            hasNextPage
                            endCursor
                        }
                        nodes {
                            path
                            additions
                            deletions
                            changeType
                        }
                    }
                }
            }
        }
    }
    """
)

query_files = gql(
    """
    query ($owner: String!, $repo: String!, $pull_number: Int!, $after_files: String) {
        repository(owner: $owner, name: $repo) {
            pullRequest(number: $pull_number) {
                files(first: 100, after: $after_files) {
                    pageInfo {
                        hasNextPage
                        endCursor
                    }
                    nodes {
                        path
                        additions
                        deletions
                        changeType
                    }
                }
            }
        }
    }
    """
)
        
has_next_page = True
after = None
has_next_page_files = True
after_files = None
pulls = []

while has_next_page:
    # fetch all pull requests
    params = {"owner": owner, "repo": repo, "after": after, "after_files": after_files}
    try:
        result = client.execute(query, variable_values=params)
    except Exception as e:
        print(e)
        print(f'Error with {len(pulls)} pulls fetched')
        print('Retrying...')
        continue
    pulls += result['repository']['pullRequests']['nodes']
    has_next_page = result['repository']['pullRequests']['pageInfo']['hasNextPage']
    after = result['repository']['pullRequests']['pageInfo']['endCursor']
    for pull in result['repository']['pullRequests']['nodes']:
        if pull['number']==51:
            print(pull)

        files = []
        # # files={"name":repo,"children":[]}
        # for file in pull['files']['nodes']:
        #     preprocess_files(file,files) 
        files += pull['files']['nodes']
        if 'pageInfo' not in pull['files'].keys():
            continue
        has_next_page_files = pull['files']['pageInfo']['hasNextPage']
        # after_files = pull['files']['pageInfo']['endCursor']
        # while has_next_page_files:
        #     # fetch all files for each pull request
            # params = {"owner": owner, "repo": repo, "pull_number": pull['number'], "after_files": after_files}
        #     try:
        #         result = client.execute(query_files, variable_values=params)
        #     except Exception as e:
        #         print(e)
        #         print(f'{len(pulls)} pulls fetched')
        #         print(f'Error with fetching files of pulls {len(pulls)}')
        #         print('Retrying...')
        #         continue
        #     # for file in result['repository']['pullRequest']['files']['nodes']:
        #         # preprocess_files(file,files)
        #     files += result['repository']['pullRequest']['files']['nodes']
        #     has_next_page_files = result['repository']['pullRequest']['files']['pageInfo']['hasNextPage']
        #     after_files = result['repository']['pullRequest']['files']['pageInfo']['endCursor']
        pull['files'] = files
    print(f'{len(pulls)} pulls fetched')

for item in pulls:
     index=index+1
     item['value']=index
# save the result into json file
with open(f'./{owner}_{repo}_pulls.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(pulls))