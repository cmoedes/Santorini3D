from constants import PLAYER_WORKERS

class Player:
    def __init__(self):
        self.workers = []
        self.captured = False
        for i in range(PLAYER_WORKERS):
            self.workers.append({"x": -1, "y":-1, "cap":False})
    
    def set_worker_position(self, worker, x, y):
        self.workers[worker]["x"] = x
        self.workers[worker]["y"] = y

    def __str__(self):
        retstr = "Player: "
        for i, worker in enumerate(self.workers):
            retstr+= f"\tWorker {i} || {worker}\n"
        return retstr


