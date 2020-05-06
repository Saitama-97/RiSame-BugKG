import json

from django.shortcuts import render
from collections import Counter
import Site.db as db
import re

# Create your views here.
# 数据库启动执行
graph = db.Neo4j()
graph.connect_neo4j()


# 图谱概览
def index(request):
    return render(request, 'index.html')


# 实体识别
def entity_recognition(request):
    return render(request, 'entity_recognition.html')


# 实体识别数据处理
def er_process(request):
    ret = {}
    print(request.POST['user_text'])
    # 实体识别程序，待完善
    # data['result'] = ?
    return render(request, 'entity_recognition.html', ret)


# 关系抽取-待完善
def relation_extract(request):
    return render(request, 'relation_extract.html')


# 关系抽取数据处理
def re_process(request):
    return None


# 判断元素是否在二维列表中
def is_exist_by_double_list(target, element):
    for line in target:
        if element in line:
            return True
    return False


# 实体查询
def search_entity(request):
    ctx = {}
    ret = {}
    ls1 = []
    flag = -1
    # 如果传来数据
    if request.GET:
        # 获取实体名称
        entity_name = request.GET['user_text']
        # 查询数据库 -> 与本实体有关系的实体及关系
        if entity_name.isdigit():  # 缺陷类实体
            flag = 0
            entity_relation = graph.get_entity_by_bugid(entity_name)
            for i in range(len(entity_relation)):
                ls2 = []
                relation = str(type(entity_relation[i]['rel'])).split('.')[-1].split("'")[0]
                entity = entity_relation[i]['t']['name']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
        else:  # 文本类实体
            flag = 1
            # i-缺陷类 | j-文本类
            entity_relation, bugT, textT = graph.get_entity_by_entity(entity_name)
            for i in range(len(bugT)):
                ls2 = []
                relation = str(type(bugT[i]['rel'])).split('.')[-1].split("'")[0]
                entity = bugT[i]['b']['ID']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
            for i in range(len(textT)):
                ls2 = []
                relation = str(type(textT[i]['rel'])).split('.')[-1].split("'")[0]
                entity = textT[i]['t1']['name']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
            print(ls1)
        if len(entity_relation) == 0:  # 数据库中没有该实体
            ctx = {'title': '<h1>数据库中暂未添加该实体</h1>'}
            return render(request, 'search_entity.html', {'ctx': json.dumps(ctx, ensure_ascii=False)})
        else:  # 数据库中有该实体
            ret['flag'] = flag
            ret['relations'] = ls1
            ret['source'] = entity_name
            return render(request, 'search_entity.html',
                          {'ret': ret})

    return render(request, 'search_entity.html')


# 实体查询数据处理
def se_process(request):
    data = {}
    return render(request, 'search_entity.html', data)


# 关系查询
def search_relation(request):
    ctx = {}
    ls1 = []
    ret = {}
    if request.GET:
        entity1 = request.GET['entity1_text']
        relation = request.GET['relation_name_text'].capitalize()
        entity2 = request.GET['entity2_text']
        # relation = relation.lower()
        # 若只输入entity1,则输出与entity1有直接关系的实体和关系[缺陷类]
        if len(entity1) != 0 and len(relation) == 0 and len(entity2) == 0:
            bugT, textT = graph.find_relation_by_entity(entity1)
            for i in range(len(bugT)):
                ls2 = []
                relation = str(type(bugT[i]['rel'])).split('.')[-1].split("'")[0]
                entity = bugT[i]['b']['ID']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
            for i in range(len(textT)):
                ls2 = []
                relation = str(type(textT[i]['rel'])).split('.')[-1].split("'")[0]
                entity = textT[i]['t']['name']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
            print(ls1)
            ret['source'] = entity1
            ret['relations'] = ls1
            return render(request, 'search_relation.html', {'ret': ret})
        # 若只输入entity2则,则输出与entity2有直接关系的实体和关系[文本类]
        elif len(entity2) != 0 and len(relation) == 0 and len(entity1) == 0:
            bugT, textT = graph.find_relation_by_entity2(entity2)
            for i in range(len(bugT)):
                ls2 = []
                relation = str(type(bugT[i]['rel'])).split('.')[-1].split("'")[0]
                entity = bugT[i]['b']['ID']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
            for i in range(len(textT)):
                ls2 = []
                relation = str(type(textT[i]['rel'])).split('.')[-1].split("'")[0]
                entity = textT[i]['t']['name']
                if not is_exist_by_double_list(ls1, entity):  # 如果二维数组里面没有此元素
                    ls2.append(relation)
                    ls2.append(entity)
                    ls1.append(ls2)
            print(ls1)
            ret['source'] = entity2
            ret['relations'] = ls1
            return render(request, 'search_relation.html', {'ret': ret})
        # 若只输入entity1和relation,则输出与entity2有直接关系的实体和关系[文本类]
        elif len(entity1) != 0 and len(relation) != 0 and len(entity2) == 0:
            bugT, textT = graph.find_relation_by_entity3(entity1, relation)
            for i in range(len(bugT)):
                ls2 = []
                id = bugT[i]['b.id']
                if not is_exist_by_double_list(ls1, id):
                    ls2.append(relation)
                    ls2.append(id)
                    ls1.append(ls2)
            for i in range(len(textT)):
                ls2 = []
                name = textT[i]['t.name']
                if not is_exist_by_double_list(ls1, name):
                    ls2.append(relation)
                    ls2.append(name)
                    ls1.append(ls2)
            print(ls1)
            ret['source'] = entity1
            ret['relations'] = ls1
            return render(request, 'search_relation.html', {'ret': ret})
        # 若只输入entity2和relation,则输出与entity2有直接关系的实体和关系[文本类]
        elif len(entity2) != 0 and len(relation) != 0 and len(entity1) == 0:
            bugT, textT = graph.find_relation_by_entity4(entity2, relation)
            for i in range(len(bugT)):
                ls2 = []
                id = bugT[i]['b.ID']
                if not is_exist_by_double_list(ls1, id):
                    ls2.append(relation)
                    ls2.append(id)
                    ls1.append(ls2)
            for i in range(len(textT)):
                ls2 = []
                name = textT[i]['t.name']
                if not is_exist_by_double_list(ls1, name):
                    ls2.append(relation)
                    ls2.append(name)
                    ls1.append(ls2)
            print(ls1)
            ret['source'] = entity1
            ret['relations'] = ls1
            return render(request, 'search_relation.html', {'ret': ret})
        # 全为空
        elif len(entity1) != 0 and len(relation) != 0 and len(entity2) != 0:
            pass
        ctx = {'title': '<h1>暂未找到相应的匹配</h1>'}
        return render(request, 'search_relation.html', {'ctx': ctx})
    return render(request, 'search_relation.html', {'ctx': ctx})


# 关系查询数据处理
def sr_process(request):
    return None


# 智能问答
def bugQA(request):
    return render(request, 'bugQA.html')


# 智能问答数据处理
def qa_process(request):
    context = {'ctx': ''}
    # 返回值
    ret = {}
    # 问题
    question = request.GET['question']
    # 问题类型
    questionType = -1
    # 问题样式
    questiontype = -1
    # 问题模板
    patternLst = [[r"what's the [a-zA-Z]+ of bug-[0-9]+",
                   r"what is the [a-zA-Z]+ of bug-[0-9]+",
                   r"Bug-[0-9]+'s [a-zA-Z]+"],
                  [r"Firefox里经常出Bug的是哪些组件"]]
    for i in range(len(patternLst)):  # lst外层-哪一类
        for j in range(len(patternLst[i])):  # lst内层-哪一个
            if re.search(patternLst[i][j], question, flags=re.IGNORECASE):
                questionType = i
                questiontype = j
                break
    # 输出具体问题编码
    print("qT -", questionType, "qt -", questiontype)
    # 问题类型-1：问属性
    if questionType == 0:
        # 属性名
        query = ""
        # BugID
        bid = ""
        if questiontype == 0 or questiontype == 1:
            res1 = re.findall(r"the [a-zA-Z]+ of", question, flags=re.IGNORECASE)[0]
            query = res1.split(' ')[1]
            res2 = re.findall(r"of bug-[0-9]+", question, flags=re.IGNORECASE)[0]
            bid = res2.split('-')[1]
        elif questiontype == 2:
            res3 = re.findall(r"'s [a-zA-Z]+", question, flags=re.IGNORECASE)[0]
            res4 = re.findall(r"bug-[0-9]+", question, flags=re.IGNORECASE)[0]
            query = res3.split(' ')[1]
            bid = res4.split('-')[1]
        print(query, '***', bid)
        # 查询数据库
        ret['answer'] = graph.query_property(query, bid)
        relations = graph.get_entity_by_bugid(bid)
        ls1 = []
        for i in range(len(relations)):
            ls2 = []
            relation = str(type(relations[i]['rel'])).split('.')[-1].split("'")[0]
            entity = relations[i]['t']['name']
            ls2.append(relation)
            ls2.append(entity)
            ls1.append(ls2)
        ret['bid'] = bid
        ret['relations'] = ls1
        # 回传数据
        if ret['answer'] != 'wu':
            if len(ret) != 0 and ret != 0:
                print("HELL", ret)
                return render(request, 'bugQA.html', {'ret': ret})
            print("HEll", context)
        else:
            return render(request, 'bugQA.html', {'ctx': '暂未找到答案'})
    elif questionType == 1:
        ls1 = []
        ls = []
        res1 = graph.get_top_component()
        for item in res1:
            ls1.append(item['b.Component'])
        for i in Counter(ls1).most_common(3):
            ls.append(i[0])
        ret['answers'] = ls
        return render(request, 'bugQA.html', {'ret': ret})
    return render(request, 'bugQA.html', ret)


# 智能搜索-待完善
def search(request):
    return render(request, 'search.html')


# 智能搜索数据处理
def search_process(request):
    return None


# 数据标注
def tag(request):
    return render(request, 'tag.html')
