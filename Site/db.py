from py2neo import Graph, Node, Relationship


class Neo4j():
    graph = None

    def __init__(self):
        print("******Starting!******")

    def connect_neo4j(self):
        self.graph = Graph("bolt://localhost:11015", username="neo4j", password="risame")
        print("******Neo4j connected!******")
        print()

    # 属性查询
    # arg：属性名，缺陷ID
    # return：查询某缺陷的属性
    def query_property(self, property_name, bid):
        try:
            answer = \
                self.graph.run(
                    "MATCH(n:Bug) WHERE n.ID ='{}' RETURN n.{} AS ret".format(bid, property_name.capitalize())).data()[
                    0][
                    'ret']
        except:
            answer = "wu"
        return answer

    # 根据缺陷id查询关联实体
    # arg：缺陷ID
    # return：与所查缺陷有关联的所有实体及关系
    def get_entity_by_bugid(self, bid):
        try:
            answer = self.graph.run(
                "MATCH (b:Bug) - [rel] - (t:Text)  WHERE b.ID = '{}' RETURN rel,t".format(bid)).data()
        except:
            answer = "wuguanlian"
        return answer

    # 根据实体查询关联实体
    # arg：实体名称
    # return：与所查实体有关联的所有实体及关系
    def get_entity_by_entity(self, entity_name):
        global answer
        try:
            answer1 = self.graph.run(
                "MATCH (b:Bug) - [rel] - (t:Text)  WHERE t.name = '{}' RETURN rel,b".format(entity_name)
            ).data()
            answer2 = self.graph.run(
                "MATCH (t1:Text) - [rel] - (t:Text)  WHERE t.name = '{}' RETURN rel,t1".format(entity_name)
            ).data()
            answer = answer1 + answer2
        except:
            answer1 = "wuguanlian"
            answer2 = "wuguanlian"
        return answer, answer1, answer2

    # 查找entity1及其对应的关系
    # arg：实体1名称
    # return：与所查实体有关联的所有实体及关系
    def find_relation_by_entity(self, entity):
        answer1 = self.graph.run(
            "MATCH (B:Bug) - [rel] - (b:Bug)  WHERE B.ID = '{}' RETURN rel,b".format(entity)
        ).data()
        answer2 = self.graph.run(
            "MATCH (B:Bug) - [rel] - (t:Text)  WHERE B.ID = '{}' RETURN rel,t".format(entity)
        ).data()
        return answer1, answer2

    def find_relation_by_entity2(self, entity):
        answer1 = self.graph.run(
            "MATCH (b:Bug) - [rel] - (T:Text)  WHERE T.name = '{}' RETURN rel,b".format(entity)
        ).data()
        answer2 = self.graph.run(
            "MATCH (t:Text) - [rel] - (T:Text)  WHERE T.name = '{}' RETURN rel,t".format(entity)
        ).data()
        return answer1, answer2

    def find_relation_by_entity3(self, entity1, relation):
        answer1 = self.graph.run(
            "MATCH (B:Bug) - [:{}] - (b:Bug)  WHERE B.ID = '{}' RETURN b.ID".format(relation.capitalize(), entity1)
        ).data()
        answer2 = self.graph.run(
            "MATCH (B:Bug) - [:{}] - (t:Text)  WHERE B.ID = '{}' RETURN t.name".format(relation.capitalize(), entity1)
        ).data()
        return answer1, answer2

    def find_relation_by_entity4(self, entity2, relation):
        answer1 = self.graph.run(
            "MATCH (b:Bug) - [:{}] - (T:Text)  WHERE T.name = '{}' RETURN b.ID".format(relation.capitalize(), entity2)
        ).data()
        answer2 = self.graph.run(
            "MATCH (t:Text) - [:{}] - (T:Text)  WHERE T.name = '{}' RETURN t.name".format(relation.capitalize(),
                                                                                          entity2)
        ).data()
        return answer1, answer2

    def get_top_component(self):
        answer = self.graph.run("match(b:Bug) return b.Component").data()
        return answer
