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
header = {
    'Authorization': f'Bearer {token}'
}
parser = argparse.ArgumentParser()
parser.add_argument("--owner", type=str, default='scikit-learn') # scikit-learn
parser.add_argument("--repo", type=str, default='scikit-learn')
args = parser.parse_args()
owner = args.owner
repo = args.repo
num=20

# use GitHub graphql API
transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=header)
client = Client(transport=transport, fetch_schema_from_transport=True)

query_commits= gql(
    """
    query ($owner: String!, $repo: String!, $after: String) {
        repository(owner: $owner, name: $repo) {
            defaultBranchRef {
                target {
                    ... on Commit {
                        history(first: 20, after: $after) {
                            totalCount
                            pageInfo {
                                hasNextPage
                                endCursor
                            }
                            nodes {
                                message
                                committedDate
                            }
                        }
                    }
                }
            }           
        }
    }
    """
)
# has_next_page = True
# after = None
# commits=[]
# commits.append({'total_commits':None})
# while has_next_page:
#     # fetch all commits
#     params = {"owner": owner, "repo": repo, "after": after}
#     try:
#         result = client.execute(query_commits, variable_values=params)
#     except Exception as e:
#         print(e)
#         print(f'Error with {len(commits)} commits fetched')
#         print('Retrying...')
#         continue
#     commits[0]['total_commits'] = result['repository']['defaultBranchRef']['target']['history']['totalCount']
#     commits += result['repository']['defaultBranchRef']['target']['history']['nodes']
#     has_next_page = result['repository']['defaultBranchRef']['target']['history']['pageInfo']['hasNextPage']
#     after = result['repository']['defaultBranchRef']['target']['history']['pageInfo']['endCursor']
#     print(f'Fetched {len(commits)} commits')
# with open(f'../assets/data/{owner}_{repo}_commits.json', "w", encoding='utf-8') as outfile:
#         outfile.write(json.dumps(commits))


query_stars= gql(
    """
    query ($owner: String!, $repo: String!, $after: String) {
        repository(owner: $owner, name: $repo) {
            stargazers(first: 20, after: $after) {
                totalCount
                pageInfo {
                    hasNextPage
                    endCursor
                }                
                edges {
                    starredAt
                    node {
                        name
                    }
                }
            }                   
        }
    }
    """
)
has_next_page = True
after = None
stars=[]
index=0
# stars.append({'total_stars':None})
while has_next_page:
    # fetch all stars
    params = {"owner": owner, "repo": repo, "after": after}
    try:
        result = client.execute(query_stars, variable_values=params)
    except Exception as e:
        print(e)
        print(f'Error with {len(stars)} stars fetched')
        print('Retrying...')
        continue
    # stars[0]['total_stars'] = result['repository']['stargazers']['totalCount']
    
    for item in result['repository']['stargazers']['edges']:
        dic={}
        dic['starredAt']=item['starredAt']
        dic['name']= None if item['node']['name'] is None else item['node']['name']
        stars.append(dic)
    has_next_page = result['repository']['stargazers']['pageInfo']['hasNextPage']
    after = result['repository']['stargazers']['pageInfo']['endCursor']
    print(f'{len(stars)} stars fetched')
for item in stars:
     index=index+1
     item['value']=index
with open(f'../assets/data/{owner}_{repo}_stars.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(stars))


query_forks= gql(
    """
    query ($owner: String!, $repo: String!, $after: String) {
        repository(owner: $owner, name: $repo) {
            forks(first: 20, after: $after, orderBy: {field: CREATED_AT, direction: ASC}) {
                totalCount
                pageInfo {
                    hasNextPage
                    endCursor
                }                
                nodes {
                    createdAt
                }
             }                  
        }
    }
    """
)

has_next_page = True
after = None
forks=[]
# forks.append(dict({'total_forks':''}))
while has_next_page:
    # fetch all forks
    params = {"owner": owner, "repo": repo, "after": after}
    try:
        result = client.execute(query_forks, variable_values=params)
    except Exception as e:
        print(e)
        print(f'Error with {len(forks)} forks fetched')
        print('Retrying...')
        continue
    # forks[0]['total_forks']= result['repository']['forks']['totalCount']
    forks += result['repository']['forks']['nodes']
    has_next_page = result['repository']['forks']['pageInfo']['hasNextPage']
    after = result['repository']['forks']['pageInfo']['endCursor']
    print(f'{len(forks)} forks fetched')
index=0
for item in forks:
     index=index+1
     item['value']=index
with open(f'../assets/data/{owner}_{repo}_forks.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(forks))

