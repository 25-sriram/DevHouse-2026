import logging
from devhouse_engine.graph.neo4j_connector import Neo4jConnector

logger = logging.getLogger(__name__)

class GraphBuilder:
    def __init__(self, connector: Neo4jConnector):
        self.connector = connector

    def build_file_dependency(self, commit_id, file_name, structure):
        """
        Processes AST structure and builds Neo4j nodes/relationships.
        """
        try:
            # Create File node
            self.connector.execute_query(
                "MERGE (f:File {name: $file_name, commit_id: $commit_id})",
                {"file_name": file_name, "commit_id": commit_id}
            )

            # Create Class nodes and relationships
            for class_name in structure.get("classes", []):
                self.connector.execute_query(
                    """
                    MERGE (c:Class {name: $class_name, commit_id: $commit_id})
                    WITH c
                    MATCH (f:File {name: $file_name, commit_id: $commit_id})
                    MERGE (f)-[:CONTAINS]->(c)
                    """,
                    {"class_name": class_name, "file_name": file_name, "commit_id": commit_id}
                )

            # Create Function nodes and relationships
            for func_name in structure.get("functions", []):
                self.connector.execute_query(
                    """
                    MERGE (fn:Function {name: $func_name, commit_id: $commit_id})
                    WITH fn
                    MATCH (f:File {name: $file_name, commit_id: $commit_id})
                    MERGE (f)-[:CONTAINS]->(fn)
                    """,
                    {"func_name": func_name, "file_name": file_name, "commit_id": commit_id}
                )

            # Create Import nodes (as Modules) and relationships
            for imp_name in structure.get("imports", []):
                self.connector.execute_query(
                    """
                    MERGE (m:Module {name: $imp_name})
                    WITH m
                    MATCH (f:File {name: $file_name, commit_id: $commit_id})
                    MERGE (f)-[:IMPORTS]->(m)
                    """,
                    {"imp_name": imp_name, "file_name": file_name, "commit_id": commit_id}
                )

            # Create Call nodes (as Functions potentially) and relationships
            for call_name in structure.get("calls", []):
                self.connector.execute_query(
                    """
                    MERGE (target:Function {name: $call_name, commit_id: $commit_id})
                    WITH target
                    MATCH (f:File {name: $file_name, commit_id: $commit_id})
                    MERGE (f)-[:CALLS]->(target)
                    """,
                    {"call_name": call_name, "file_name": file_name, "commit_id": commit_id}
                )

            logger.info(f"Graph dependencies built for {file_name}")
        except Exception as e:
            logger.error(f"Failed to build graph for {file_name}: {e}")
