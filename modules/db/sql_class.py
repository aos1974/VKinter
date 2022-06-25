import sqlalchemy

from modules.utils import utils

class SqlClass:
    def __init__(self):
        self.db = utils.get_token("db_connection")
        self.engine = sqlalchemy.create_engine(self.db)
        self.connection = self.engine.connect()

    def get_test(self, id):
        sql = f"""
        SELECT name FROM test WHERE id={id};
        """
        result = self.connection.execute(sql).fetchall()
        return result[0][0]

