from sqlalchemy import create_engine
from sqlalchemy import text


def df_to_db(df, table_name):
    """Convert a Pandas Dataframe to a Database.
        Args:
            df: pd.DataFrame which is to be converted to a database
            table_name: String containing the name of the table
        Returns:
            DB: SQLAlchemy DB object
    """
    db = create_engine(f'sqlite:///:memory:', echo=False)
    df.to_sql(name=table_name, con=db, index=False)
    return db


def handle_response(response):
    """Handles the response from OpenAI.

    Args:
        response (JSON Object): Response from OpenAI

    Returns:
        String: SQL Query
    """
    query = response["choices"][0]["text"]
    if query.startswith(" "):
        query = "Select" + query
    elif query.startswith("Select"):
        pass
    else:
        query = "Select " + query
    return query


def execute_sql_query(db, query):
    """Execute a query on a database.

    Args:
        db (SQLAlchemy db): database engine
        query (String): Our query to be executed

    Returns:
        list: The results of the query contained in a list
    """
    with db.connect() as con:
        result = con.execute(text(query))
        return result.fetchall()
