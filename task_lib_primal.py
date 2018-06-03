from abc import ABCMeta, abstractclassmethod, abstractproperty

class abstract_tasker:
    __metaclass__=ABCMeta

    @abstractclassmethod
    def get_task():
        """get task for task pull"""


    @abstractclassmethod
    def add_answer():
        """add answer to answer pull"""

# primal numbers solver
def solve(task):
    if task == 'NO_TASK':
        return 'NO_TASK'
    task = int(task)
    number = 2
    divider_count = 0
    while number <= task:
        if task % number == 0:
            divider_count+=1
        if divider_count > 1:
            return str(''+str(task)+' '+str(False))
        number +=1
    return str(''+str(task)+' '+str(True)) 

class tsker(abstract_tasker):

    initial_len = 0
    tasks = []
    answers = []

    def __init__(self, tasks):
        self.tasks = tasks
        self.initial_len = len(tasks)

    def get_task(self):
        if len(self.tasks) < 1:
            return str('NO_TASK')
        return str(self.tasks.pop(0))

    def add_answer(self, answer):
        self.answers.append(answer)

    def status(self):
        return ('{0:.2f}%'.format(len(self.answers)/self.initial_len))
