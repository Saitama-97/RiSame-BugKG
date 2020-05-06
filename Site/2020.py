from py2neo import Graph, Node, Relationship

graph = Graph("bolt://localhost:11015", username="neo4j", password="risame")

# answer = self.graph.run("MATCH(n:Bug) WHERE n.ID ='{}' RETURN n.{}".format(bid, property_name)).data()

answer = graph.run("MATCH(n:Bug) WHERE n.ID ='1571747' RETURN n.Component AS ret").data()[0]
print(answer['ret'])
print(answer.get('Component'))
