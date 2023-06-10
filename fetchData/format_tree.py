import json

with(open('../assets/data/modelmapper_modelmapper.json','r',encoding='utf-8')) as f:
    data = json.load(f)['pulls']
def access_tree_add_delete(children):
    for item in children:
        if 'children' in item.keys():
            access_tree_add_delete(item['children'])
            item['addition']=0
            item['deletion']=0
            if 'children' in item.keys():
                for child in item['children']:
                    item['addition']+=child['addition']
                    item['deletion']+=child['deletion']
for item in data:
    item = item['files']
    if 'children' in item.keys():
        access_tree_add_delete(item['children'])
        


    