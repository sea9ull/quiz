# from .db import execute, select, selectOne

class User():
    users = {}

    def getAnswer(self, id, qid):
        hasAnswer = id in self.users and qid in self.users[id]["answers"]
        result = False
        if hasAnswer:
            result = self.users[id]["answers"][qid]
        return hasAnswer, result

    def setAnswer(self, data):
        answers = self.users[data["id"]]["answers"]
        hasAnswer = data["qid"] in answers
        if not hasAnswer:
            answers[data["qid"]] = (data["result"], data["answer"])

    def userCheck(self, data):
        hasUser = data["id"] in self.users
        if not hasUser:
            self.setUser(data)

    def setUser(self, data):
        self.users[data["id"]] = {"name": data["name"], "answers": {}}

    def deleteAllAnswer(self):
        self.users = {}

    def totalScore(self):
        score = []
        for id in self.users:
            u = self.users[id]
            ans = []
            total = 0
            for qid in range(12):
                hasAnswer = qid in u["answers"]
                answer = False
                if hasAnswer:
                    answer = u["answers"][qid][0]
                if answer:
                    total += 1
                ans.append(answer)
            record = {
                "id": id,
                "name": u["name"],
                "q1": ans[0],
                "q2": ans[1],
                "q3": ans[2],
                "q4": ans[3],
                "q5": ans[4],
                "q6": ans[5],
                "q7": ans[6],
                "q8": ans[7],
                "q9": ans[8],
                "q10": ans[9],
                "q11": ans[10],
                "q12": ans[11],
                "total": total
            }
            score.append(record)
        byTotal = [i["total"] for i in l]
        return sorted(score, key=byTotal, reverse=False)
