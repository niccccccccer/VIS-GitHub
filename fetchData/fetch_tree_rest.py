import requests
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--owner", type=str, default='d3') # scikit-learn
parser.add_argument("--repo", type=str, default='d3')
args = parser.parse_args()
owner = args.owner
repo = args.repo
headers = {
    'Accept': 'application/vnd.github+json',
    'Authorization': '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',
    'X-GitHub-Api-Version': '2022-11-28'
}
commit_num='37b1960e0af52d12bc7bbea2ed932ea954c36d14'
url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/{commit_num}?recursive=1'

response = requests.get(url, headers=headers)

with open(f'../assets/data/{owner}_{repo}_tree.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(response.json()))


with open(f'../assets/data/{owner}_{repo}_tree.json', "r") as f:
    data = json.load(f)
tree = data['tree']
format={'name':repo,'children':[]}  #格式化后的tree

# def access_tree(tree,item,tmp,current):  #tree是格式化的tree,item是源数据,tmp是分割后的path,current是path的第几层
#     if current==len(tmp)-1:
#         if type=='blob':
#             tree[tmp[current]]={'type':item['type'],'mode':item['mode'],'size':item['size']}
#         else:
#             tree[tmp[current]]={'type':item['type'],'mode':item['mode']}
#     else:
#         current+=1
#         access_tree(tree[tmp[current-1]],item,tmp,current)

def access_tree(tree,item,tmp,current):  #tree是格式化的tree,item是源数据,tmp是分割后的path,current是path的第几层
    if current==len(tmp)-1:
        if item['type']=='blob':
            tree['children'].append({'name':tmp[current],'path':item['path'],'type':item['type'],'mode':item['mode'],'value':item['size']})
        else:
            tree['children'].append({'name':tmp[current],'path':item['path'],'type':item['type'],'mode':item['mode'],'children':[]})
    else:
        for child in tree['children']:
             if child['name']==tmp[current]:
                 access_tree(child,item,tmp,current+1)


# def add_size(node):
#     if "children" in node:
#         children = node["children"]
#         size = sum(add_size(child) for child in children)
#     else:
#         size = node.get("size", 0)
#     node["size"] = size
#     return size

for item in tree:
    tmp = item['path'].split("/")
    access_tree(format,item,tmp,0)

# add_size(format)
# print(format)  
with open(f'../assets/data/{owner}_{repo}_tree_format.json', "w", encoding='utf-8') as outfile:
        outfile.write(json.dumps(format))
        


# for item in tree:
#     if item['type'] == 'blob':
#         if item['mode']!='100644':
#             print(item)
#     elif item['type'] == 'tree':
#         if item['mode']!='040000':
#             print(item)
#     else:
#         print(item)
#--------100755 blob