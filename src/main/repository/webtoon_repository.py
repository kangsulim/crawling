import mariadb

class WebtoonRepository:

    host = "localhost"
    port = 3306
    user = "root"
    password = "123456"
    database = "webtoon"

    @classmethod
    def insertMany(cls, webtoons):
        connection = mariadb.connect(
            host=cls.host,
            port=cls.port,
            user=cls.user,
            password=cls.password,
            database=cls.database
        )
        cursor = connection.cursor()


        sql = """
            insert into webtoon_tb
            values (default, ?, ?, ?, ?, ?)
        """

        cursor.executemany(sql, webtoons)

        connection.commit()
        cursor.close()
        connection.close()