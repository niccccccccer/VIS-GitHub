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
parser.add_argument("--owner", type=str, default='scikit-learn') # scikit-learn
parser.add_argument("--repo", type=str, default='scikit-learn')
args = parser.parse_args()
owner = args.owner
repo = args.repo
index=0
data_all={}
# use GitHub graphql API
transport = AIOHTTPTransport(url="https://api.github.com/graphql", headers=header)
client = Client(transport=transport, fetch_schema_from_transport=True)
params = {"owner": owner, "repo": repo}

#-------------------------------basic information---------------------------------
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
try:
    data_all = client.execute(query_basic, variable_values=params)['repository']
except Exception as e:
    print(e)
    print('Retrying...')

# -------------------------------------fetch all pull requests--------------
query = gql(
    """
    query ($owner: String!, $repo: String!, $after: String, $after_files: String) {
        repository(owner: $owner, name: $repo) {
        description
        homepageUrl
            pullRequests(first: 20, after: $after) {
                pageInfo {
                    hasNextPage
                    endCursor
                }
                nodes {
                    number
                    title
                    body
                    url
                    createdAt
                    closedAt
                    mergedAt
                    updatedAt
   
                    state
                    author {
                        login
                    }
                    authorAssociation
                    baseRefName
                    totalCommentsCount
                    closingIssuesReferences{
                        totalCount
                    }
                    commits(first: 30){
                        totalCount
                        nodes{
                            commit{
                                abbreviatedOid
                                }
                        }
                        
                    }
                    labels(first: 30) {
                        nodes {
                            name
                        }
                    }
                    THUMBS_UP: reactions(content: THUMBS_UP) {
                        totalCount
                    }
                    THUMBS_DOWN: reactions(content: THUMBS_DOWN) {
                        totalCount
                    }
                    LAUGH: reactions(content: LAUGH) {
                        totalCount
                    }
                    HOORAY: reactions(content: HOORAY) {
                        totalCount
                    }
                    CONFUSED: reactions(content: CONFUSED) {
                        totalCount
                    }
                    HEART: reactions(content: HEART) {
                        totalCount
                    }
                    ROCKET: reactions(content: ROCKET) {
                        totalCount
                    }
                    EYES: reactions(content: EYES) {
                        totalCount
                    }
                    milestone {
                        title
                    }
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
    """
)

reaction_keys = ['THUMBS_UP', 'THUMBS_DOWN', 'LAUGH', 'HOORAY', 'CONFUSED', 'HEART', 'ROCKET', 'EYES']
# remove zero reactions
def reactions(pull):
    reactions = {}
    for key in pull.keys():
        if key in reaction_keys:
            reactions[key] = pull[key]['totalCount']
    return reactions

def preprocess_except_files(pull):
    pull['labels'] = [label['name'] for label in pull['labels']['nodes']]
    pull['author'] = pull['author'] if pull['author'] is None else pull['author']['login']
    pull['closingIssuesReferences'] = pull['closingIssuesReferences']['totalCount']
    pull['totalCommit']=   pull['commits']['totalCount']
    pull['commits'] = [commit['commit']['abbreviatedOid'] for commit in pull['commits']['nodes']]
    pull['milestone'] = pull['milestone']['title'] if pull['milestone'] else None
    pull['reactions'] = reactions(pull)
    for reaction in reaction_keys:
        if reaction in pull.keys():
            del pull[reaction]
    return pull

def access_tree(item,tmp,current,files):  #item是源数据,tmp是分割后的path,current是path的第几层,files是格式化后的所有文件
    if current==len(tmp)-1:
        files['children'].append({'name':tmp[current],'addition':item['additions'],'deletion':item['deletions'],'changeType':item['changeType']})
    else:
        exist=False
        # print(type(files))
        # print(files)
        for child in files['children']:
            if child['name']==tmp[current]:
                 exist=True
                 access_tree(item,tmp,current+1,child)
        if not exist:
            files['children'].append({'name':tmp[current],'children':[]})
            access_tree(item,tmp,current+1,files['children'][-1])

def preprocess_files(file,files):
    tmp = file['path'].split("/")
    access_tree(file,tmp,0,files)
        
# def access_tree_add_delete(children):
#     for item in children:
#         if 'children' in item.keys():
#             access_tree_add_delete(item['children'])
#             item['addition']=0
#             item['deletion']=0
#             if 'children' in item.keys():
#                 for child in item['children']:
#                     item['addition']+=child['addition']
#                     item['deletion']+=child['deletion']

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
        pull = preprocess_except_files(pull)
        # files = []
        files={"name":repo,"children":[]}
        for file in pull['files']['nodes']:
            preprocess_files(file,files) 
        # if 'children' in files.keys():
        #     access_tree_add_delete(files['children'])
        #     for child in files['children']:
        #             files['addition']+=child['addition']
        #             files['deletion']+=child['deletion']
            
        # files += pull['files']['nodes']
        if 'pageInfo' not in pull['files'].keys():
            continue
        has_next_page_files = pull['files']['pageInfo']['hasNextPage']
        after_files = pull['files']['pageInfo']['endCursor']
        while has_next_page_files:
            # fetch all files for each pull request
            params = {"owner": owner, "repo": repo, "pull_number": pull['number'], "after_files": after_files}
            try:
                result = client.execute(query_files, variable_values=params)
            except Exception as e:
                print(e)
                print(f'{len(pulls)} pulls fetched')
                print(f'Error with fetching files of pulls {len(pulls)}')
                print('Retrying...')
                continue
            for file in result['repository']['pullRequest']['files']['nodes']:
                preprocess_files(file,files)
            # if 'children' in files.keys():
            #     access_tree_add_delete(files['children'])
            # files += result['repository']['pullRequest']['files']['nodes']
            has_next_page_files = result['repository']['pullRequest']['files']['pageInfo']['hasNextPage']
            after_files = result['repository']['pullRequest']['files']['pageInfo']['endCursor']
        pull['files'] = files
        after_files = None  # reset after_files!!!
    print(f'{len(pulls)} pulls fetched')

for item in pulls:
     index=index+1
     item['value']=index
data_all['pulls']=pulls

#--------------stars--------------------------------
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
data_all['stars']=stars

#--------------forks--------------------------------
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
data_all['forks']=forks


# save the result into json file
with open(f'../assets/data/{owner}_{repo}.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(data_all))