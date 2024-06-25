import sqlite3
from sqlite3 import Connection, Cursor
from typing import Iterator, Optional, Union

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas import DataFrame, Series
from tqdm import tqdm


def loadTableIntoDataframe(
    conn: Connection,
    tableName: str,
    columns: Optional[list] = None,
    returnIterator: bool = False,
) -> pd.DataFrame:
    columns_str = "*" if columns is None else ", ".join(columns)
    query = f"SELECT {columns_str} FROM {tableName}"

    # Execute the query and read the result into a pandas DataFrame
    if returnIterator:
        df = pd.read_sql_query(query, conn, chunksize=50000)
    else:
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


def plotNodesVsRelationships(conn: Connection) -> None:
    nodeCount = countNodes(conn)
    relationshipCount = countRelationships(conn)
    data = {"": ["Nodes", "Relationships"], "Count": [nodeCount, relationshipCount]}
    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)
    # Plotting using seaborn
    plt.figure(figsize=(8, 6))
    sns.barplot(data=df, x="", y="Count")
    plt.ylabel("Count")
    plt.title("Node Count vs Relationship Count")
    plt.tight_layout()
    plt.savefig(
        "/Users/karolinaryzka/Documents/neo4jQueries/src/nodesVsRelationships.png"
    )


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


def inDegreeCentrality(conn: Connection) -> pd.DataFrame:
    query = f"SELECT ref_oaid, Count(*) as c FROM relationship_cites GROUP BY ref_oaid HAVING Count(*) > 15 ORDER BY c DESC LIMIT 15;"
    result = pd.read_sql_query(query, conn)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=result, x="ref_oaid", y="c")
    plt.xlabel("OPEN ALEX ID")
    plt.ylabel("In-Degree Centrality")
    plt.title("Top 15 Most Cited Papers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("/Users/karolinaryzka/Documents/neo4jQueries/src/inDegree.png")
    return result


def outDegreeCentrality(conn: Connection) -> pd.DataFrame:
    query = f"SELECT work_oaid, Count(*) as c FROM relationship_cites GROUP BY work_oaid HAVING Count(*) > 15 ORDER BY c DESC LIMIT 15;"
    result = pd.read_sql_query(query, conn)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=result, x="work_oaid", y="c")
    plt.xlabel("OPEN ALEX ID")
    plt.ylabel("Out-Degree Centrality")
    plt.title("Top 15 Papers that Reference Others")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("/Users/karolinaryzka/Documents/neo4jQueries/src/outDegree.png")
    return result


def isolatedNodes(conn: Connection) -> pd.DataFrame:
    query = f"SELECT ref_oaid, Count(*) as c FROM relationship_cites GROUP BY ref_oaid HAVING Count(*) = 1;"
    result = pd.read_sql_query(query, conn)
    return result


def singletonNodes(conn: Connection) -> pd.DataFrame:
    query = f"SELECT ref_oaid, Count(*) as c FROM relationship_cites GROUP BY ref_oaid HAVING Count(*) IS NULL;"
    result = pd.read_sql_query(query, conn)
    return result


def mostFrequentDegreeCounts(conn: Connection) -> pd.DataFrame:
    query = f"""
    SELECT degree_count, COUNT(*) AS frequency
    FROM (
        SELECT work_oaid, COUNT(*) AS degree_count
        FROM relationship_cites
        GROUP BY work_oaid
    ) AS degree_counts
    GROUP BY degree_count
    ORDER BY frequency DESC LIMIT 15;
    """
    result = pd.read_sql_query(query, conn)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=result, x="degree_count", y="frequency")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.title("Top 15 Most Frequent Number of Citations")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        "/Users/karolinaryzka/Documents/neo4jQueries/src/mostFrequentDegrees.png"
    )
    return result


def nodesOfDegreeX(conn: Connection, degreeCount: int) -> pd.DataFrame:
    query = f"SELECT ref_oaid FROM relationship_cites GROUP BY ref_oaid HAVING COUNT(*) = {degreeCount};"
    result = pd.read_sql_query(query, conn)
    return result


def mostConnectedNodes(conn: Connection) -> pd.DataFrame:
    query = f"""
    SELECT node_id, SUM(degree_count) AS total_degree
    FROM (
        SELECT ref_oaid AS node_id, COUNT(*) AS degree_count
        FROM relationship_cites
        GROUP BY ref_oaid
        UNION ALL
        SELECT work_oaid AS node_id, COUNT(*) AS degree_count
        FROM relationship_cites
        GROUP BY work_oaid
    ) AS combined_degrees
    GROUP BY node_id
    HAVING SUM(degree_count) > 15
    ORDER BY total_degree DESC LIMIT 15;
    """
    result = pd.read_sql_query(query, conn)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=result, x="node_id", y="total_degree")
    plt.xlabel("OPEN ALEX ID")
    plt.ylabel("Total Degrees (in both directions)")
    plt.title("Top 15 Most Connected Papers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(
        "/Users/karolinaryzka/Documents/neo4jQueries/src/mostConnectedNodes.png"
    )
    return result


def main() -> None:
    conn = sqlite3.connect("/Users/karolinaryzka/Documents/neo4jQueries/works_cites.db")
    print(f"Number of nodes: {countNodes(conn)}")
    print(f"Number of relationships: {countRelationships(conn)}")
    plotNodesVsRelationships(conn)
    print(f"Graph density: {graphDensity(conn)}")
    print(f"Most Cited Papers: {inDegreeCentrality(conn)}")
    print(f"Papers with the Most References: {outDegreeCentrality(conn)}")
    print(f"Isolated Nodes: {isolatedNodes(conn)}")
    print(f"Singleton Nodes: {singletonNodes(conn)}")
    print(f"Most Frequent Degree Counts: {mostFrequentDegreeCounts(conn)}")
    print(f"Nodes with Degree of 10: {nodesOfDegreeX(conn, 10)}")
    print(f"Most Connected Nodes (in both directions): {mostConnectedNodes(conn)}")
    conn.close()


if __name__ == "__main__":
    main()
