from constants import PLAYER_WORKERS, BOARD_SIZE, BASE_WORKER_OBJ

class Player:
    def __init__(self):
        self.workers = []
        self.captured = False
    
    @staticmethod
    def get_empty_cell(Board):
        print("Player Worker Initialization:")
        x_pos = int(input(f"\tEnter Worker x: "))
        y_pos = int(input(f"\tEnter Worker y: "))
        
        on_board = (x_pos>=0 or x_pos<BOARD_SIZE) or (y_pos>=0 or y_pos<BOARD_SIZE)
        occupied = Board.schema[y_pos][x_pos]<0
        while(not on_board or occupied):
            print("Invalid Selection. Please try again.")
            x_pos = int(input(f"\tEnter Worker x: "))
            y_pos = int(input(f"\tEnter Worker y: "))
        return x_pos, y_pos
    
    def set_worker_position(self, worker, x, y):
        self.workers[worker] = {**self.workers[worker], "x": x, "y": y}

    def init_workers(self, Board):
        for worker in range(PLAYER_WORKERS):
            x_pos, y_pos = Player.get_empty_cell(Board)
            self.workers.append(BASE_WORKER_OBJ.copy())
            self.set_worker_position(worker, x_pos, y_pos)
            Board.history.append({})
            Board.update_schema()

    def __str__(self):
        st = "Player: \n"
        for i, worker in enumerate(self.workers):
            st+= f"\t|Worker{i}|: {worker}\n"
        return st


