# coding=utf-8


def get_user_key(conn, user):
    with conn.cursor() as cursor:
        sql = "SELECT `key` FROM `user` WHERE `user`=%s"
        cursor.execute(query=sql, args=[user])
        item = cursor.fetchone()
        if item:
            return item[0]
        else:
            return ''
