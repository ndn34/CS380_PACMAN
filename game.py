"""
turn_pacman_one_dot_score.py
Turn-based Pac-Man with ONE dot.
-1 point per move
+100 for eating the dot
"""
import pacman


BLACK=(0,0,0); WHITE=(255,255,255); YELLOW=(255,200,0)
BLUE=(40,40,255); RED=(230,30,30)

class Player:
    def __init__(self, state):
        self.state =state
        
    def get_dir(self):
        raise NotImplementedError

class Ghost_red():
    def __init__(self, state):
        self.state = state

    def get_dir(self):    
        best_move = None
        # Find the move that gets closest to Pac-Man
        min_distance = float('inf')

        for dir in self.state.get_available_dirs(self.state.ghost):
            next = pacman.Loc(self.state.ghost.x + dir[0], self.state.ghost.y + dir[1])
            
            distance =  next.distance(self.state.pac)
            if distance < min_distance:
                min_distance = distance
                best_move = dir
        # pacman.pygame.time.wait(100)
        return best_move

class Game:
    def __init__(self, state = pacman.State(pacman.RAW_MAP)):
        self.state = state

    # Main game loop
    def play(self, agent):
        ghost= Ghost_red(self.state)   
        env = pacman.Env(self.state)

        while True:
            dir = agent.get_dir()
            if dir is not None and not self.state.game_over():
                # Pacman move                
                self.state.move_pac(dir)
                # # Ghost move
                
                ghost_dir = ghost.get_dir()
                if ghost_dir is not None and not self.state.game_over(): 
                    self.state.move_ghost(ghost_dir)
                # print(f"Pacman moved {pacman.get_direction_name(dir)}, Ghost moved {pacman.get_direction_name(ghost_dir)}")
                self.state.score += self.state.reward()

            # Draw
            env.draw()

