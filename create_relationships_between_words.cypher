// 名詞(n)
MATCH (w1:Word {pos:"n"})-->(Sence1:Synset)<--(w2:Word {pos:"n"})
WITH DISTINCT w1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: ""}]->(w2)
RETURN type(r)

MATCH (w1:Word {pos:"n"})-->(Sence2:Synset)-[r1:REL_SEMANTIC_LINK]->(Sence3:Synset)<--(w2:Word {pos:"n"})
WITH DISTINCT w1, r1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: r1.relType}]->(w2)
RETURN type(r1)

// 動詞(v)
MATCH (w1:Word {pos:"v"})-->(Sence1:Synset)<--(w2:Word {pos:"v"})
WITH DISTINCT w1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: ""}]->(w2)
RETURN type(r)

MATCH (w1:Word {pos:"v"})-->(Sence2:Synset)-[r1:REL_SEMANTIC_LINK]->(Sence3:Synset)<--(w2:Word {pos:"v"})
WITH DISTINCT w1, r1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: r1.relType}]->(w2)
RETURN type(r1)

// 形容詞(a)
MATCH (w1:Word {pos:"a"})-->(Sence1:Synset)<--(w2:Word {pos:"a"})
WITH DISTINCT w1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: ""}]->(w2)
RETURN type(r)

MATCH (w1:Word {pos:"a"})-->(Sence2:Synset)-[r1:REL_SEMANTIC_LINK]->(Sence3:Synset)<--(w2:Word {pos:"a"})
WITH DISTINCT w1, r1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: r1.relType}]->(w2)
RETURN type(r1)

// 形容動詞(r)
MATCH (w1:Word {pos:"r"})-->(Sence1:Synset)<--(w2:Word {pos:"r"})
WITH DISTINCT w1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: ""}]->(w2)
RETURN type(r)

MATCH (w1:Word {pos:"r"})-->(Sence2:Synset)-[r1:REL_SEMANTIC_LINK]->(Sence3:Synset)<--(w2:Word {pos:"r"})
WITH DISTINCT w1, r1, w2
MERGE (w1)-[r:REL_WORD_SEMANTIC_LINK {relType: r1.relType}]->(w2)
RETURN type(r1)