import psycopg2
import psycopg2.extras

POSTGRES_PASSWORD = "lachlan"

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password=POSTGRES_PASSWORD,
    port="5432"  # Default PostgreSQL port
)

def run_query(query_sql):
    cur = conn.cursor()
    cur.execute(query_sql)
    conn.commit()

def get_query(query_sql):
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(query_sql)
    rows = cur.fetchall()
    return rows

def init_schema():
    run_query("""
              CREATE SCHEMA IF NOT EXISTS doc_sched
              """)
    run_query("""
              CREATE TABLE IF NOT EXISTS doc_sched.periods (
              type TEXT,
              user_name TEXT,
              year INT,
              month INT,
              date DATE,
              slot TEXT
              )
              """)
    run_query("""
              CREATE TABLE IF NOT EXISTS doc_sched.users (
              id TEXT,
              type TEXT,
              first_name TEXT,
              last_name TEXT,
              ft_fraction NUMERIC
              )
              """) 

def check_period_exists(period):
    query_sql = f"""
        SELECT user_name, year, month, date, slot
        FROM doc_sched.periods
        WHERE user_name='{period["user"]}'
        AND year={period["year"]}
        AND month={period["month"]}
        AND date='{period["date"]}'
        AND slot='{period["slot"]}'
        AND type='{period["type"]}'
        """
    results = get_query(query_sql)
    if len(results) == 0:
        return False
    else:
        return True
    
def add_period(period):
    query_sql = f"""
        INSERT INTO doc_sched.periods (type, user_name, year, month, date, slot)
        VALUES ('{period["type"]}', '{period["user"]}', {period["year"]}, {period["month"]}, '{period["date"]}', '{period["slot"]}')
        """
    run_query(query_sql)

def get_periods(user, year, month):
    query_sql = f"""
        SELECT type, user_name, year, month, date, slot
        FROM doc_sched.periods
        WHERE user_name='{user}'
        AND year={year}
        AND month={month}
        """
    return get_query(query_sql)

def delete_period(period):
    query_sql = f"""
        DELETE FROM doc_sched.periods
        WHERE user_name='{period["user_name"]}'
        AND year={period["year"]}
        AND month={period["month"]}
        AND date='{period["date"]}'
        AND slot='{period["slot"]}'
        AND type='{period["type"]}'
        """
    run_query(query_sql)

def get_users():
    query_sql = f"""
        SELECT id, type, first_name, last_name, ft_fraction
        FROM doc_sched.users
        """
    return get_query(query_sql)