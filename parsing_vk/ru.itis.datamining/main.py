from DbWorker import DbWorker


def run():
    import vk
    db_worker = DbWorker(db_name='postgres',
                         db_password='gev56poison',
                         db_host='datamining-db.cojbnxf0wpbv.us-east-1.rds.amazonaws.com',
                         db_user='postgres',
                         db_port=5432)

    db_worker.execute_query("truncate top_words")

    token = "a208acdca208acdca208acdcf9a27e1555aa208a208acdcc249a356c1626f7970e58fe7"  # Сервисный ключ доступа
    session = vk.Session(access_token=token)  # Авторизация
    vk = vk.API(session)

    dic = {}

    for i in range(2):
        data = vk.wall.get(domain="itis_kfu", offset=i * 100, count=100, v=5.92)
        for item in data['items']:
            split = item['text'].split(" ")
            for j in split:
                lowerWord = str(j).lower()
                if lowerWord in dic:
                    dic[lowerWord] += 1
                else:
                    dic[lowerWord] = 1

    sorted_list = sorted(dic, key=dic.get, reverse=True)

    top_list = {}
    for i in range(100):
        word = sorted_list[i]
        top_list[word] = dic[word]

    for key, value in top_list.items():
        db_worker.execute_query(query="insert into top_words values ('" + key + "', " + str(value) + ");")
