# import json
# import io
# import sys
# data=[]
# owner="modelmapper"
# repo="modelmapper"
# with open(f'../assets/data/{owner}_{repo}_pulls.json', "r") as f:
#     data = json.load(f)
# # Corpus with example sentences
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')         #改变标准输出的默认编码
# print(data)
for i in range(0,10):
    print(i)
# corpus = data['title']
# print(corpus)
#  timelineItems(first: 40, after: $after_files) {
#                         pageInfo {
#                             hasNextPage
#                             endCursor
#                         }
#                         nodes {
                            
#                             first,
#                             itemTypes,
#                             last
#                         }
#                     }



# query {
#   repository(owner: "modelmapper", name: "modelmapper") {
#     createdAt
#     stargazerCount
#     forkCount
#     pullRequests(first: 20) {
#       totalCount
#       nodes {
#         title
#         createdAt
#       }
#     }
#     defaultBranchRef {
#       target {
#         ... on Commit {
#           history(first: 30) {
#             totalCount
#             nodes {
#               message
#               committedDate
#             }
#           }
#         }
#       }
#     }
#   }
# }


# 查询star人name和时间---------------------------
# {
#   repository(owner: "modelmapper", name: "modelmapper") {
#     stargazers(first: 100) {
#       edges {
#         starredAt
#     	}
#       nodes {
#           name
#       }
#     }
#   }
# }

# {
#   repository(owner: "modelmapper", name: "modelmapper") {
#     forkCount
#     milestones(first: 20) {
#       nodes {
#         closed
#         closedAt
#         createdAt
#         dueOn
#         number
#         state
#         updatedAt
#       }
#     }
#   }
# }


# {
#   repository(owner: "modelmapper", name: "modelmapper") {
    # defaultBranchRef {
    #   target {
    #     ... on Commit {
    #       history(first: 30) {
    #         totalCount
    #         nodes {
    #           message
    #           committedDate
    #         }
    #       }
    #     }
    #   }
    # }
#     pullRequests(first:100){
#       totalCount
#       nodes{
#       	createdAt
#       }
#     }
    # forks(first: 100, orderBy: {field: CREATED_AT, direction: ASC}) {
    #   totalCount
    #   nodes {
    #     createdAt
    #   }
    # }
    # stargazers(first: 100) {
    #   totalCount
    #   edges {
    #     starredAt
    #   }
    #   nodes {
    #     name
    #   }
    # }
#   }
# }

