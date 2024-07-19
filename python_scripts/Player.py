from constants import PLAYER_WORKERS, BOARD_SIZE, BASE_WORKER_OBJ, DIRS

class Player:
    def __init__(self):
        self.workers = []
        self.captured = False
        self.won = False
    
    @staticmethod
    def get_empty_cell(Board):
        print("Player Worker Initialization:")

        x_pos = int(input(f"\tEnter Worker x: "))
        y_pos = int(input(f"\tEnter Worker y: "))
        on_board = (x_pos>=0 and x_pos<BOARD_SIZE) and (y_pos>=0 and y_pos<BOARD_SIZE)
        valid = on_board and (Board.schema[y_pos][x_pos]['Player'] is None)

        while(not valid):
            print("Invalid Selection. Please try again.")
            x_pos = int(input(f"\tEnter Worker x: "))
            y_pos = int(input(f"\tEnter Worker y: "))
            on_board = (x_pos>=0 and x_pos<BOARD_SIZE) and (y_pos>=0 and y_pos<BOARD_SIZE)
            valid = on_board and (Board.schema[y_pos][x_pos]['Player'] is None)
        return x_pos, y_pos
    
    def get_valid_move(self, Board):
        valid_moves = self.find_valid_moves(Board)
        selection = [] #Might remove this later, append directly to board.
        if(not valid_moves):
            self.captured = True
            return False

        worker_valid, worker_selected = False, None
        move_valid, move_selected = False, None
        build_valid, build_selected = False, None

        while(not worker_valid):
            print("\nPlayer Selecting Worker: ")
            for worker_num in valid_moves:
                print(f"{worker_num}. WORKER {worker_num}")
            worker_selected = int(input("Input Selected Worker Number: "))
            if(worker_selected in valid_moves):
                worker_valid = True
                print(f"Player Selected Worker Number {worker_selected}")
            else:
                print("\nInput Invalid. Please input valid worker number.")
        
        worker_moves = valid_moves[worker_selected]
        while(not move_valid):
            print("\nPlayer Selecting Worker Move: ")
            for i, move in enumerate(worker_moves):
                print(f"{i}. MOVE: x:{move['x']}, y:{move['y']}")
            move_selected = int(input("Input Selected Move Number: "))

            if(move_selected<len(worker_moves) and move_selected>=0):
                move_valid = True
                print(f"Player Selected Move Number {move_selected}")
            else:
                print("\nInput Invalid. Please input valid move number.")

        move = worker_moves[move_selected]
        selection.append({'type': move['type'], 'Player': move['Player'], 'Worker':move['Worker'],'x':move['x'], 'y': move['y']})
        Board.history.append({'type': move['type'], 'Player': move['Player'], 'Worker':move['Worker'],'x':move['x'], 'y': move['y']})
        Board.update_schema()
        
        self.check_win_condition(Board)
        if(self.won):
            return selection

        worker_builds = move['next']
        
        while(not build_valid):
            print("\nPlayer Selecting Worker Build:")
            for i, build in enumerate(worker_builds):
                print(f"{i}. BUILD: x:{build['x']}, y:{build['y']}")
            build_selected = int(input("Input Selected Build Number: "))

            if(build_selected<len(worker_builds) and build_selected>=0):
                build_valid = True
                print(f"Player Selected Move Number {build_selected}")
            else:
                print("\nInput Invalid. Please input valid build number.")

        build = worker_builds[build_selected]
        selection.append({'type': build['type'], 'Player': build['Player'], 'Worker':build['Worker'], 'x':build['x'], 'y': build['y']})
        Board.history.append({'type': build['type'], 'Player': build['Player'], 'Worker':build['Worker'], 'x':build['x'], 'y': build['y']})
        Board.update_schema()
        return selection
    
    def set_worker_position(self, worker_num, x_pos, y_pos):
        self.workers[worker_num] = {'x': x_pos, 'y': y_pos}

    def init_workers(self, Board):
        for worker_num in range(PLAYER_WORKERS):
            x_pos, y_pos = self.get_empty_cell(Board)
            self.workers.append(BASE_WORKER_OBJ.copy())
            Board.history.append({'type':'set', 'Player':self, 'Worker':worker_num, 'x':x_pos, 'y':y_pos})
            Board.update_schema()

    def find_valid_moves(self, Board):
        valid_moves = {}
        for worker_num, worker in enumerate(self.workers):
            valid_moves[worker_num] = []
            x, y = list(worker.values())
            
            for x_off, y_off in DIRS:
                xm, ym = x+x_off, y+y_off
                move_on_board = xm>=0 and ym>=0 and xm<BOARD_SIZE and ym<BOARD_SIZE
                valid_height = move_on_board and (Board.schema[y][x]['Height']-Board.schema[ym][xm]['Height'])>=-1 and Board.schema[ym][xm]['Height']<4
                cell_unoccupied = move_on_board and Board.schema[ym][xm]['Worker'] is None
                
                if(valid_height and cell_unoccupied):

                    valid_moves[worker_num].append({'type':'move', 'Player':self, 'Worker':worker_num, 'x':xm, 'y':ym, 'next':[]})
                    for x_offb, y_offb in DIRS:
                        xb, yb = xm+x_offb, ym+y_offb
                        build_on_board = xb>=0 and yb>=0 and xb<BOARD_SIZE and yb<BOARD_SIZE
                        valid_heightb = build_on_board and (Board.schema[ym][xm]['Height']-Board.schema[yb][xb]['Height'])>=0 and Board.schema[yb][xb]['Height']<4
                        cell_unoccupiedb = build_on_board and (Board.schema[yb][xb]['Worker'] is None or Board.schema[yb][xb]['Worker'] == worker_num)
                        
                        if(valid_heightb and cell_unoccupiedb):
                            valid_moves[worker_num][-1]['next'].append({'type': 'build', 'Player':self, 'Worker':worker_num, 'x':xb, 'y':yb})
                    
                    if(not valid_moves[worker_num][-1]['next']):
                        del valid_moves[worker_num][-1]

            if(not valid_moves[worker_num]):
                del valid_moves[worker_num]
        
        return valid_moves or False

    def check_win_condition(self, Board):
        player_won = False
        other_players_captured = True

        for worker in self.workers:
            x, y = worker['x'], worker['y']
            if(Board.schema[y][x]['Height'] == 3):
                player_won = True
        
        for Player in Board.Players:
            if(Player is not self and (not Player.captured)):
                other_players_captured = False

        player_won = player_won or other_players_captured
        if(not Board.game_over and player_won):
            print("\nPlayer worker has reached height of 3 or all other players are captured. Player wins!")
            Board.game_over = True
            self.won = True
    
    def execute_turn(self, Board):
        print(Board)
        print("Player Executing Turn")
        self.check_win_condition(Board)
        if(not Board.game_over):
            player_move = self.get_valid_move(Board)
            if(not player_move):
                print("Player is/was captured and can no longer perform any moves.")
                return
            #Board.history.extend(player_move)
            Board.update_schema()
            self.check_win_condition(Board)

    def __str__(self):
        st = "Player: "
        for worker_num, worker in enumerate(self.workers):
            st+= f"\n\t|Worker{worker_num}|: {worker}"
        return st


