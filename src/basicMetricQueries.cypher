//Degree Centrality
MATCH (n)
WITH n, size([(n)-->() | 1]) AS degree
RETURN n, degree AS numberOfConnections
ORDER BY degree DESC
LIMIT 1

//Degree Centrality (5)
CALL gds.degree.stream('graph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId) , score AS mostCited
ORDER BY mostCited DESC, nodeId LIMIT 5


//Degree Distribution
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
RETURN degree, COUNT(*) AS frequency
ORDER BY degree ASC

//Distribution of x connections
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
WHERE degree = 10
RETURN n AS numberOfNodesWithDegree10
LIMIT 10

//Graph Density
MATCH (n)
WITH COUNT(n) AS numNodes
MATCH ()-->()
WITH numNodes, count(*) AS numRelationships
RETURN 2.0 * numRelationships / (numNodes * (numNodes - 1)) AS desnity

//Graph Instance
CALL gds.graph.project(
  'graph', 
  '*',     
  'RELATED' 
)


//Isolated Nodes
MATCH (n)
WHERE size([(n)--() | 1]) = 0
RETURN n AS isolatedNodes

// Memory Estimation
CALL gds[.<tier>].<algorithm>.<execution-mode>.estimate(
  graphNameOrConfig: String or Map,
  configuration: Map //same as target alg 
) YIELD
  nodeCount: Integer,
  relationshipCount: Integer,
  requiredMemory: String,
  treeView: String,
  mapView: Map,
  bytesMin: Integer,
  bytesMax: Integer,
  heapPercentageMin: Float,
  heapPercentageMax: Float

//Most Connected Node
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
RETURN n, degree AS numberOfConnections
ORDER BY degree DESC
LIMIT 1

//Most Frequency Degree Counts
MATCH (n)
WITH size([(n)--() | 1]) AS degree
RETURN degree, COUNT(*) AS frequency 
ORDER BY frequency DESC
LIMIT 1

//Number of Nodes
MATCH (n)
RETURN COUNT(n) as numberOfNodes

//Number of Relationships
MATCH ()-->()
RETURN count(*) AS numberOfRelationships

//Singleton Nodes
MATCH (n)
WHERE size([(n)--() | 1]) = 1
RETURN n AS singletonNodes

//Top 10 Degrees
MATCH (n)
WITH n, size([(n)--() | 1]) AS degree
RETURN n, degree
ORDER BY degree DESC
LIMIT 10