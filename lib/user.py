from .db import execute, select, selectOne


def getAnswer(id, qid):
    sql = "select id, qid, result from user_answer where id = %s and qid = %s"
    row = selectOne(sql, (id, qid))

    hasAnswer = not (row is None)
    result = False
    if hasAnswer:
        result = row['result']
    return hasAnswer, result


def setAnswer(data):
    hasAnswer, _ = getAnswer(data["id"], data["qid"])
    if not hasAnswer:
        sql = "insert into user_answer(id, qid, result, answer) values (%s, %s, %s, %s)"
        params = (data["id"], data["qid"], data["result"], data["answer"])
        execute(sql, params)


def userCheck(data):
    sql = "select id, name from user_info where id = %s"
    row = selectOne(sql, (data["id"]))
    if row is None:
        setUser(data)


def setUser(data):
    sql = "insert into user_info(id, name) values (%s, %s)"
    params = (data["id"], data["name"])
    execute(sql, params)


def deleteAllAnswer():
    execute("delete from user_answer")


def totalScore():
    sql = """
    select u.id as id, u.name as name,
    sum(case when a.qid = 0 then a.result else 0 end) as q1,
    sum(case when a.qid = 1 then a.result else 0 end) as q2,
    sum(case when a.qid = 2 then a.result else 0 end) as q3,
    sum(case when a.qid = 3 then a.result else 0 end) as q4,
    sum(case when a.qid = 4 then a.result else 0 end) as q5,
    sum(case when a.qid = 5 then a.result else 0 end) as q6,
    sum(case when a.qid = 6 then a.result else 0 end) as q7,
    sum(case when a.qid = 7 then a.result else 0 end) as q8,
    sum(case when a.qid = 8 then a.result else 0 end) as q9,
    sum(case when a.qid = 9 then a.result else 0 end) as q10,
    sum(case when a.qid = 10 then a.result else 0 end) as q11,
    sum(case when a.qid = 11 then a.result else 0 end) as q12,
    sum(a.result) as total
    from user_info as u, user_answer as a
    where u.id = a.id
    group by u.id, u.name
    order by `total` desc
"""
    return select(sql)
