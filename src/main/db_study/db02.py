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

    dataList = [
        ("월", "title1", "author1", "6.4", "imgUrl1"),
        ("화", "title2", "author2", "8.6", "imgUrl2"),
        ("수", "title3", "author3", "9.4", "imgUrl3")
    ]

    sql = """
        insert into webtoon_tb
        values (default, ?, ?, ?, ?, ?)
    """

    cursor.executemany(sql, dataList)

    connection.commit()