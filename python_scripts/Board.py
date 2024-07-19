from constants import BOARD_SIZE, TOTAL_PLAYERS, PLAYER_WORKERS, BASE_CELL_OBJ
from Player import Player

class Board:
    def __init__(self):
        self.history_pointer = 0
        self.history = []
        self.schema = []
        self.Players = []
        self.game_over = False

    def init_schema(self):
        for row in range(BOARD_SIZE):
            self.schema.append([BASE_CELL_OBJ.copy() for _ in range(BOARD_SIZE)])

    def init_players(self):
        for i in range(TOTAL_PLAYERS):
            self.Players.append(Player())
            self.Players[i].init_workers(self)
            
    def simulate_game(self):
        self.init_schema()
        self.init_players()
        player_turn = 0
        while(not self.game_over):
            player_turn = player_turn % TOTAL_PLAYERS
            self.Players[player_turn].execute_turn(self)
            player_turn+=1
        print("Player won. Game Over.")

    def update_schema(self):
        for i in range(self.history_pointer, len(self.history)):
            event = self.history[i]
            
            if(event['type'] == 'set'):
                x, y = event['x'], event['y']
                self.schema[y][x]['Player'] = event['Player']
                self.schema[y][x]['Worker'] = event['Worker']
                event['Player'].set_worker_position(event['Worker'], event['x'], event['y'])
            
            elif(event['type'] == 'move'):
                Worker = event['Player'].workers[event['Worker']]
                xw, yw, x, y = Worker['x'], Worker['y'], event['x'], event['y']
                self.schema[yw][xw]['Player'] = None
                self.schema[yw][xw]['Worker'] = None
                self.schema[y][x]['Player'] = event['Player']
                self.schema[y][x]['Worker'] = event['Worker']
                event['Player'].set_worker_position(event['Worker'], event['x'], event['y'])
            
            elif(event['type'] == 'build'):
                x, y = event['x'], event['y']
                self.schema[y][x]['Height'] = self.schema[y][x]['Height'] + 1
                
        self.history_pointer = len(self.history)

    def reset(self):
        self.history_pointer = 0
        self.history.clear()
        self.schema.clear()
        self.Players.clear()
        self.game_over = False

    def __str__(self):
        st="\n"
        for row in self.schema:
            for cell in row:
                item = str(cell['Height']) or "0"
                if(cell['Player'] is not None):
                    item = "X"
                st+=item
            st+="\n"
        return st