"""
agents
"""

import game
import pacman
import sys
import random
from collections import defaultdict
import pickle

def defaultDictFunc():
    return {d: 0.0 for d in pacman.DIRS}

class Human(game.Player):
    def __init__(self, state):
        super().__init__(state)

    def get_dir(self):
        dir = None
        # Check for quit events
        for e in pacman.pygame.event.get():
            if e.type==pacman.pygame.QUIT: sys.exit()
            if e.type==pacman.pygame.KEYDOWN:
                if e.key==pacman.pygame.K_ESCAPE: sys.exit()
                if e.key==pacman.pygame.K_UP:    dir = pacman.UP
                if e.key==pacman.pygame.K_DOWN:  dir = pacman.DOWN
                if e.key==pacman.pygame.K_LEFT:  dir = pacman.LEFT
                if e.key==pacman.pygame.K_RIGHT: dir = pacman.RIGHT
                return dir          
    
class Random(game.Player):
    def __init__(self, state):
        super().__init__(state)

    def get_dir(self):
        dir= None
        # Check for quit events
        for e in pacman.pygame.event.get():
            if e.type==pacman.pygame.QUIT: sys.exit()
            if e.type==pacman.pygame.KEYDOWN:
                if e.key==pacman.pygame.K_ESCAPE: sys.exit()
        # Pick dir
        available_dir = self.state.get_available_dirs(self.state.pac) #all the legal directions
        r = random.random()
        dir = random.choice(available_dir)
        if self.state.game_over():
            self.state.reset()
        pacman.pygame.time.wait(100)
        # print(f"Available dirs: {[pacman.get_direction_name(d) for d in available_dir]}")
        return dir

class QPlayer(game.Player):
    def __init__(self, state, epsilon=0.1,gamma=0.9,alpha=0.8):
        super().__init__(state)
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = gamma
        self.q_table_id = defaultdict(defaultDictFunc) # set up q table, func here is at the top
        

    def get_QValue(self, state_id, dir):
        """
          Returns Q(state,dir)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        return self.q_table_id[state_id][dir]
    
    def compute_value_from_QValues(self, state_id):
        """
          Returns max_dir Q(state,dir)
          where the max is over legal dirs.  Note that if
          there are no legal dirs, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        available_dir = self.state.get_available_dirs(pacman.Loc(state_id[0], state_id[1])) # get available dirs
        if len(available_dir) == 0: # if no choices return 0.0
            return 0.0
        val = self.get_QValue(state_id, available_dir[0]) # set first value
        for i in range(len(available_dir)-1): # loop over remaining values
            temp = self.get_QValue(state_id, available_dir[1+i])
            if temp > val: val = temp # save value if Q value is larger
        return val

    def compute_dir_from_QValues(self, state_id):
        """
          Compute the best dir to take in a state.  Note that if there
          are no legal dirs, which is the case at the terminal state,
          you should return None.
        """
        available_dir = self.state.get_available_dirs(pacman.Loc(state_id[0], state_id[1])) # get available dirs
        if len(available_dir) == 0: # if no choices return 0.0
            return None
        bestDir = available_dir[0] # set first dir
        bestVal = self.get_QValue(state_id, bestDir) # set first dir's qval
        for i in range(len(available_dir)-1): # loop over remaining values
            temp = self.get_QValue(state_id, available_dir[1+i])
            if temp > bestVal: # if new qval is >
                bestVal = temp # save value if Q value is larger
                bestDir = available_dir[1+i] # save dir if qval is >
        return bestDir
    
    def get_dir_epolicy(self):
        """
          Compute the dir to take in the current state.  With
          probability self.epsilon, we should take a random dir and
          take the best policy dir otherwise.  Note that if there are
          no legal dirs, which is the case at the terminal state, you
          should choose None as the dir.

          HINT: To pick randomly from a list, use random.choice(list)
        """
        
        # If game is over, reset the state 
        if self.state.game_over():
            return None
            
        # Check for quit events
        for e in pacman.pygame.event.get():
            if e.type==pacman.pygame.QUIT: sys.exit()
            if e.type==pacman.pygame.KEYDOWN:
                if e.key==pacman.pygame.K_ESCAPE: sys.exit()
        
        #your code here
        state_id = self.state.get_state_id() # get state id
        available_dir = self.state.get_available_dirs(self.state.pac)
        
        if len(available_dir) == 0: return None
        elif random.random() < self.epsilon: # random from 0 to 1 is less than the epsilon, return a random move
            return random.choice(available_dir)
        else:
            return self.compute_dir_from_QValues(state_id) # generate dir from Q values

    def update(self, state_id, dir, nextState_id, reward):
        """
          You should do your Q-Value update here
        """
        # 𝑄(𝑆, 𝐴) ← (1 − 𝛼)𝑄(𝑆, 𝐴) + 𝛼[𝑅 + 𝛾 max𝐴′𝑄(𝑆′, 𝐴′)]
        self.q_table_id[state_id][dir] = (1 - self.alpha) * self.get_QValue(state_id, dir) + self.alpha * (reward + self.discount * self.compute_value_from_QValues(nextState_id))

    def print_q_table(self):
        """
          Print the Q-table
        """
        for state_id, val in self.q_table_id.items():
            print("State:(" + f"{state_id[0]}, {state_id[1]}, {state_id[2]}, {state_id[3]})" + f" UP: {round(val[pacman.UP], 2)} DOWN: {round(val[pacman.DOWN], 2)} LEFT: {round(val[pacman.LEFT], 2)} RIGHT: {round(val[pacman.RIGHT], 2)}")

    def save_q_table(self, file_path):
        """
          Save the Q-table to a file
        """
        with open(file_path, "wb") as f: # saving to file
            pickle.dump(self.q_table_id, f)

    def learn_episodes(self, episodes = None, file_path = None):
        if episodes is None:
            print("Number of episodes not provided. Using default value of 1000.")
            episodes = 1000
        if file_path is None:
            print("File path not provided. Using default value of 'qtable.pkl'.")
            file_path = "qtable.pkl"
        env = pacman.Env(self.state)
        episode_count = 1
        ghost = game.Ghost_red(self.state) # create ghost for proper gamestates
        while True:
            for e in pacman.pygame.event.get():
                if e.type==pacman.pygame.QUIT: 
                    self.print_q_table()
                    # Save the dictionary
                    self.save_q_table(file_path)
                    sys.exit()
                    
                if e.type==pacman.pygame.KEYDOWN:
                    if e.key==pacman.pygame.K_ESCAPE:
                        self.print_q_table()
                        # Save the dictionary
                        self.save_q_table(file_path)
                        sys.exit()
            
            env.msg_from_agent = f"Episode: {episode_count}/{episodes}"

            #your code here
            if self.state.game_over() and episode_count < episodes: # if game over, BUT more episodes, increment episode count and reset gamestate
                episode_count += 1
                self.state.reset()
                continue
            elif not self.state.game_over(): # if game is  not over
                initialState = self.state.get_state_id() 
                newDir = self.get_dir_epolicy()
                self.state.move_pac(newDir) #these 3 lines update state
                if not self.state.game_over(): self.state.move_ghost(ghost.get_dir()) # only move ghost if game isnt over, can screw with points otherwise
                newState = self.state.get_state_id() 
                reward = self.state.reward()
                self.update(initialState, newDir, newState, reward) #update in table

            # Draw            
            if self.state.game_over() and episode_count >= episodes:
                env.msg_from_agent = f"Training complete!! Exit to save Q-table!"
            env.draw()
            
            
                

    def upload_q_table(self, file_path =None):
        """
          Load the Q-table from a file
        """
        if file_path is None: # default to this to avoid crash
            file_path = "qtable.pk1"
        with open(file_path, "rb") as f:
            self.q_table_id = pickle.load(f)
        
    def get_dir(self):
        if not self.q_table_id:
            print("Q-table is empty. Please load a Q-table before playing.")
            return sys.exit()

        # Check for quit events
        for e in pacman.pygame.event.get():
            if e.type==pacman.pygame.QUIT: 
                self.print_q_table()
                sys.exit()
            if e.type==pacman.pygame.KEYDOWN:
                if e.key==pacman.pygame.K_ESCAPE: 
                    self.print_q_table()
                    sys.exit()
        # Pick dir
        state_id = self.state.get_state_id() 
        if self.state.game_over():
            dir = None
        else: dir = self.compute_dir_from_QValues(state_id)
        pacman.pygame.time.wait(200)
        return dir

        
