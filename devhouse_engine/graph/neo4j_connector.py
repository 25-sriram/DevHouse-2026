from neo4j import GraphDatabase
import logging
from devhouse_engine.config.settings import settings

logger = logging.getLogger(__name__)

class Neo4jConnector:
    def __init__(self):
        self._uri = settings.NEO4J_URI
        self._user = settings.NEO4J_USER
        self._password = settings.NEO4J_PASSWORD
        self._driver = None
        self.connect()

    def connect(self):
        try:
            self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
            self._driver.verify_connectivity()
            logger.info("Connected to Neo4j successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self._driver = None

    def close(self):
        if self._driver:
            self._driver.close()

    def execute_query(self, query, parameters=None):
        if not self._driver:
            logger.error("Neo4j driver not initialized.")
            return None
            
        try:
            with self._driver.session() as session:
                return session.run(query, parameters)
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None
