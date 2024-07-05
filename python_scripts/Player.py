from constants import PLAYER_WORKERS

class Player:
    def __init__(self):
        self.workers = []
        self.captured = False
        for i in range(PLAYER_WORKERS):
            self.workers.append({
                "x": -1, 
                "y":-1,
                "cap":False
            })
    
    def set_worker_positions(self, workers, positions):
        if(type(workers) is list):
            for i, (worker, position) in enumerate(zip(workers, positions)):
                self.workers[worker]["x"] = position["x"]
                self.workers[worker]["y"] = position["y"]
            return
        self.workers[workers]["x"] = positions["x"]
        self.workers[workers]["y"] = positions["y"]
    
    def get_valid_moves(self, Board):
        valid_moves = {}
        board_schema = Board.get_schema()
        for worker in self.workers:
            pass
        return valid_moves
    
    def execute_move(self, Board):
        pass
    def __str__(self):
        print("Player:")
        for i, worker in enumerate(self.workers):
            print(f"\tWorker ${i} - (x, y): (${worker["x"]}, ${worker["y"]})")


