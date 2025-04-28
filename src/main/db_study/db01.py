import mariadb

if __name__ == '__main__':
    connection = mariadb.connect(
        host="localhost",
        port=3306,
        user="root",
        password="123456",
        database="webtoon"
    )

    cursor = connection.cursor()
    sql = """
    insert into webtoon_tb
    values
        (default, '월', 'test', 'test_author', '9.9', '이미지url')
    """

    cursor.execute(sql)

    connection.commit() # commit()을 작성해야 DB에 저장됨