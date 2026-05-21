from datetime import timedelta
from sqlalchemy import text
from db.connection import db_connect

# https://docs.sqlalchemy.org/en/21/core/connections.html#sqlalchemy.engine.Connection.execute
def thirtyDayCount():
    engine = db_connect()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT MAX(consult_time) FROM hourly_data"))
        maior_data = result.scalar()

        if maior_data is None:
            return

        range30days = maior_data - timedelta(days=30)
        conn.execute(text("DELETE FROM hourly_data WHERE consult_time < :todelete"),{"todelete": range30days})
        conn.commit()
