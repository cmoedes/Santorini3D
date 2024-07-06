from constants import BOARD_SIZE, TOTAL_PLAYERS, PLAYER_WORKERS
from Player import Player

class Board:
    def __init__(self):
        self.history_pointer = 0
        self.history = []
        self.schema = []
        self.Players = []
        self.game_Over = False

    def init_schema(self):
        for row in range(BOARD_SIZE):
            self.schema.append([0]*BOARD_SIZE)

    def init_players(self):
        for i in range(TOTAL_PLAYERS):
            self.Players.append(Player())
            self.Players[i].init_workers(self)
            
    def simulate_game(self):
        self.init_schema()
        self.init_players()

    def update_schema(self):
        pass

    def Reset(self):
        self.history.clear()
        self.schema.clear()
        self.Players.clear()
        self.game_over = False

    def __str__(self):
        return self.schema