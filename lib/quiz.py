import json
from enum import Enum


class QState(Enum):
    SELECT = 0
    QUESTION = 1
    ANSWER = 2
    FINISHED = 3
    START = 4

    def next(self):
        if self.value == 4:
            v = 0
        elif self.value == 3:
            v = 3
        else:
            regular_state_nums = 3
            v = (self.value + 1) % regular_state_nums
        return QState(v)


class Quiz:
    state = QState(4)
    idx = 0
    questions = []
    answers = []
    titles = []

    def __init__(self, json_path):
        with open(json_path, 'r') as f:
            obj = json.load(f)
            self.questions = [{"title": o['title'], "question": o['question'], "columns": o['columns']} for o in obj]
            self.answers = [{"answer": o['answer'], "text": o['answer_text']} for o in obj]
            self.titles = [{"title": o['title'], "enable": True} for o in obj]
        self.state = QState(4)

    def reset(self):
        self.state = QState(4)
        self.idx = 0
        for i in range(len(self.titles)):
            self.titles[i]["enable"] = True

    def checkFinished(self):
        self.titles[self.idx]['enable'] = False
        isFinished = True
        for title in self.titles:
            if title["enable"]:
                isFinished = False
                break
        if isFinished:
            self.state = QState.FINISHED

    def select(self, qid):
        if self.state == QState.SELECT:
            self.setId(qid)
        if self.state == QState.ANSWER:
            self.checkFinished()
        self.state = self.state.next()

    def next(self):
        self.select(self.idx+1)

    def judgeAnswer(self, answer):
        if self.idx >= len(self.questions):
            print("Error: invalid index")
        result = True
        for i, correct in enumerate(self.answers[self.idx]["answer"]):
            if answer[i] in correct:
                pass
            else:
                result = False
                break
        return result

    def getId(self):
        return self.idx

    def setId(self, qid):
        qid = int(qid)
        if 0 <= qid and qid < len(self.titles):
            self.idx = qid

    def getState(self):
        return self.state.name

    def getMasterState(self):
        data = None
        if self.state == QState.SELECT:
            data = self.titles
        if self.state == QState.QUESTION:
            data = self.questions[self.idx]
        if self.state == QState.ANSWER:
            data = self.answers[self.idx]
        return self.state.name, data

    def getUserState(self):
        data = None
        if self.state == QState.QUESTION:
            data = self.questions[self.idx]
        if self.state == QState.ANSWER:
            data = self.answers[self.idx]["text"]
        return self.state.name, data


# if __name__ == "__main__":
#     quiz = Quiz("resources/data/questions.json")
#     print(quiz.getState())
#     quiz.next()
#     print(quiz.getState())
#     quiz.next()
#     print(quiz.getState())
#     quiz.next()
#     print(quiz.getState())
#     quiz.next()
#     print(quiz.getState())
#     quiz.next()
#     print(quiz.getState())
