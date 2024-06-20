import pandas as pd 
import sqlite3
from typing import Optional
from tqdm import tqdm
from sqlite3 import Connection, Cursor
from pandas import DataFrame



def loadTableIntoDataframe(conn: Connection, tableName: str, columns: Optional[list] = None) -> pd.DataFrame:
    
    columns_str = "*" if columns is None else ", ".join(columns)
    query = f"SELECT {columns_str} FROM {tableName}"
    
    # Execute the query and read the result into a pandas DataFrame
    df = pd.read_sql_query(query, conn)
    
    return df

def countNodes(conn: Connection) -> int:
    query = f"SELECT COUNT(oaid) FROM works"
    result: Cursor = conn.execute(query)
    return result.fetchone()[0]
    
def countRelationships(conn: Connection) -> int:
    query = f"SELECT COUNT(*) AS numberOfRelationships FROM relationship_cites"
    result: Cursor = conn.execute(query)
    return result.fetchone()[0]

def graphDensity(conn: Connection) -> float:
    nodeCount = countNodes(conn)
    relationshipCount = countRelationships(conn)
    query = f"""
    WITH
        node_count AS (
            SELECT {nodeCount} AS numNodes
        ),
        relationship_count AS (
            SELECT {relationshipCount} AS numRelationships
        )
    SELECT 2.0 * rc.numRelationships / (nc.numNodes * (nc.numNodes - 1)) AS density
    FROM node_count nc, relationship_count rc
    """
    result: Cursor = conn.execute(query)
    return result.fetchone()[0]

def degreeCentrality(conn: Connection, nodesDf: pd.DataFrame, relationshipsDf: pd.DataFrame) -> pd.DataFrame:
    nodesDf['oaid'] = nodesDf['oaid'].astype('str')
    relationshipsDf['id'] = relationshipsDf['id'].astype('str')

    total_Steps = len(nodesDf) + len(relationshipsDf)
    with  tqdm(total=total_Steps, desc="Processing DataFrames") as pbar:
        mergedDf = nodesDf.merge(relationshipsDf, how='left', left_on='oaid', right_on='work_oaid')
        pbar.update(len(nodesDf))
        degreeCentralityDf = mergedDf.groupby('oaid').size().reset_index(name='numberOfConnections')
        pbar.update(len(relationshipsDf))
        degreeCentralityDf = degreeCentralityDf.sort_values(by='numberOfConnections', ascending=False)

    highestDegreeNode = degreeCentralityDf.head(1)
    result = highestDegreeNode
    return result

def isolatedNodes(conn: Connection, nodesDf: pd.DataFrame, relationshipsDf: pd.DataFrame) -> pd.DataFrame:
    nodesDf['oaid'] = nodesDf['oaid'].astype(str)
    relationshipsDf['work_oaid'] = relationshipsDf['work_oaid'].astype(str)

    with tqdm(total=len(nodesDf), desc="Finding Isolated Nodes") as pbar:
        mergedDf = nodesDf.merge(relationshipsDf, how='left', left_on='oaid', right_on='work_oaid')
        pbar.update(len(nodesDf))

        isolatedNodesDf = mergedDf[(mergedDf['work_oaid'].isna()) & (mergedDf['id'].isna())]
        pbar.update(len(relationshipsDf))

    return isolatedNodesDf[['oaid']]

def singletonNodes(conn: Connection, nodesDf: pd.DataFrame, relationshipsDf: pd.DataFrame) -> pd.DataFrame:
    nodesDf['oaid'] = nodesDf['oaid'].astype(str)
    relationshipsDf['work_oaid'] = relationshipsDf['work_oaid'].astype(str)

    with tqdm(total=len(nodesDf), desc="Finding Singleton Nodes") as pbar:
        mergedDf = nodesDf.merge(relationshipsDf, how='left', left_on='oaid', right_on='work_oaid')
        pbar.update(len(nodesDf))

        singletonNodesDf = mergedDf.groupby('oaid').size().reset_index(name='count')
        singletonNodesDf = singletonNodesDf[singletonNodesDf['count'] == 1]

    return singletonNodesDf[['oaid']]

def mostFrequentDegreeCounts(conn: Connection, nodesDf: pd.DataFrame, relationshipsDf: pd.DataFrame) -> pd.DataFrame:
    nodesDf['oaid'] = nodesDf['oaid'].astype(str)
    relationshipsDf['work_oaid'] = relationshipsDf['work_oaid'].astype(str)

    with tqdm(desc="Finding Most Frequent Degree Counts") as pbar:
        mergedDf = nodesDf.merge(relationshipsDf, how='left', left_on='oaid', right_on='work_oaid')
        pbar.update(len(nodesDf))

        degree_counts_df = mergedDf.groupby('oaid').agg(degree=('work_oaid', 'count')).reset_index()
        frequency_df = degree_counts_df.groupby('degree').size().reset_index(name='frequency')
        frequency_df = frequency_df.sort_values(by='frequency', ascending=False).head(10)

    return frequency_df

def nodesOfDegreeX(conn: Connection, degree: int, nodesDf: pd.DataFrame, relationshipsDf: pd.DataFrame) -> pd.DataFrame:
    nodesDf['oaid'] = nodesDf['oaid'].astype(str)
    relationshipsDf['start_node'] = relationshipsDf['work_oaid'].astype(str)

    with tqdm(desc=f"Finding Nodes with Degree {degree}") as pbar:
        mergedDf = nodesDf.merge(relationshipsDf, how='left', left_on='oaid', right_on='work_oaid')
        pbar.update(len(nodesDf))

        degreeCountsDf = mergedDf.groupby('oaid').agg(degree_count=('work_oaid', 'count')).reset_index()
        specific_degree_nodes_df = degreeCountsDf[degreeCountsDf['degree_count'] == degree].head(10)

    return specific_degree_nodes_df[['oaid']]

def main(  
) -> None:
    #db: Connection = connectToDB(dbPath)
    conn = sqlite3.connect("/Users/karolinaryzka/Documents/neo4jQueries/works_cites.db")
    print(f"Number of nodes: {countNodes(conn)}")
    print(f"Number of relationships: {countRelationships(conn)}")
    print(f"Graph density: {graphDensity(conn)}")

    nodesDf = loadTableIntoDataframe(conn, 'works', columns=['oaid'])
    relationshipsDf = loadTableIntoDataframe(conn, 'relationship_cites', columns=['id', 'work_oaid'])
    #print(f"Highest Degree Node: {degreeCentrality(conn, nodesDf, relationshipsDf)}")
    #print(f"Isolated Nodes: {isolatedNodes(conn, nodesDf, relationshipsDf)}"
    #print(f"Singleton Nodes: {singletonNodes(conn, nodesDf,relationshipsDf)}")
    #print(f"Most Frequent Degree Counts: {mostFrequentDegreeCounts(conn, nodesDf, relationshipsDf)}")
    print(f"Nodes with Degree of 10: {nodesOfDegreeX(conn, 10, nodesDf, relationshipsDf)}")
    conn.close()
    


if __name__ == "__main__":
    main()