from psycopg2.extras import NamedTupleCursor


def insert_into_db(connect, requirement, values):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(requirement, values)


def select_one_from_db(connect, requirement, values):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(requirement, values)

        data = cursor.fetchone()
        return data


def select_many_from_db(connect, requirement, values):
    with connect.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(requirement, values)

        data = cursor.fetchall()
        return data
