"""
turn_pacman_one_dot_score.py
Turn-based Pac-Man with ONE dot.
-1 point per move
+100 for eating the dot
"""

import pygame
from collections import defaultdict

RAW_MAP = [
"111111111111111111",
"111111111111111111",
"100000000010000001",
"100000000010000001",
"101110010010001001",
"100000010010100001",
"101010010010000101",
"100010010000000001",
"100000010000010001",
"111111111111111111",
]


BLACK=(0,0,0); WHITE=(255,255,255); YELLOW=(255,200,0)
BLUE=(40,40,255); RED=(230,30,30)

UP=(0,-1); DOWN=(0,1); LEFT=(-1,0); RIGHT=(1,0)
DIRS=[UP,DOWN,LEFT,RIGHT]

# Create a dictionary mapping the tuples to their names
direction_names = {
    UP: "UP",
    DOWN: "DOWN",
    LEFT: "LEFT",
    RIGHT: "RIGHT"
}

def get_direction_name(direction_tuple):
    """
    Returns the string name for a given direction tuple.

    Args:
        direction_tuple: A tuple representing a direction (e.g., (0, 1)).

    Returns:
        The string name (e.g., "DOWN") or None if the tuple is not found.
    """
    return direction_names.get(direction_tuple, None)


class Loc:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class State:
    def __init__(self, raw_map = RAW_MAP):
        self.raw_map = raw_map
        self.GRID_W, self.GRID_H = len(raw_map[0]),len(raw_map)
        self.pac = Loc(1,2)
        self.ghost = Loc(self.GRID_W-3,self.GRID_H-2)
        self.dot = Loc(self.GRID_W-2, 2)
        self.score = 0
        self.GRID=[[1 if c=="1" else 0 for c in r] for r in raw_map]

    def move_pac(self, dir):
        nx,ny=self.pac.x+dir[0],self.pac.y+dir[1]
        if self.walk(nx,ny): self.pac.x,self.pac.y=nx,ny

    def move_ghost(self,dir):
        # Ghost move
        nx,ny=self.ghost.x+dir[0],self.ghost.y+dir[1]
        if self.walk(nx,ny): self.ghost.x,self.ghost.y=nx,ny

    
    # Check if a position is walkable
    def walk(self,x,y): 
        return 0<=x<self.GRID_W and 0<=y< self.GRID_H and self.GRID[y][x]==0
    
    def reward(self):
        if self.pac_on_ghost():
            return -100
        # Check dot
        elif self.pac_on_dot():
            return 100
        else:
            return -1  # Move cost 
    
    def pac_on_dot(self):
        return self.pac.x==self.dot.x and self.pac.y == self.dot.y

    def pac_on_ghost(self):
        return self.pac.x==self.ghost.x and self.pac.y == self.ghost.y
    
    def game_over(self):
        return self.pac_on_dot() or self.pac_on_ghost()

    def reset(self):
        self.__init__(raw_map = self.raw_map)
        self.score = 0

    def get_available_dirs(self, loc):
        available = []
        for DIR in DIRS:
            nx,ny=loc.x+DIR[0],loc.y+DIR[1]
            if self.walk(nx,ny): available.append(DIR)
        return available

    def print_locations(self):
        print(f"Pac-Man is at ({self.pac.x}, {self.pac.y})")
        print(f"Ghost is at ({self.ghost.x}, {self.ghost.y})")


    def get_state_id(self):
        # Tuple for use as a key
        return (self.pac.x, self.pac.y, self.ghost.x, self.ghost.y)


class Env:
    def __init__(self, state = State(RAW_MAP)):
        self.state = state
        self.TILE = 24
        SCREEN_W, SCREEN_H = state.GRID_W*self.TILE, state.GRID_H*self.TILE
        pygame.init()
        self.screen=pygame.display.set_mode((SCREEN_W,SCREEN_H))
        self.font=pygame.font.SysFont(None,24)
        pygame.display.set_caption("One-Dot Pac-Man — Score Mode")
        self.msg_from_agent = ""

    def draw(self):
        TILE = self.TILE
        self.screen.fill(BLACK)
        for y in range(self.state.GRID_H):
            for x in range(self.state.GRID_W):
                if self.state.GRID[y][x]==1:
                    pygame.draw.rect(self.screen,BLUE,(x*TILE,y*TILE,TILE,TILE))
        
        # Dot display
        if not self.state.pac_on_dot():
            pygame.draw.circle(self.screen,WHITE,(self.state.dot.x*TILE+TILE//2, self.state.dot.y*TILE+TILE//2),4)

        # Characters display
        
        # draw the pacman as a yellow circle
        pygame.draw.circle(self.screen,YELLOW,(self.state.pac.x*TILE+TILE//2,self.state.pac.y*TILE+TILE//2),TILE//2-2)

        # Load the ghost image
        ghost_image = pygame.image.load("pacman_ghost.jpg").convert_alpha()
        # Resize the image using pygame.transform.scale() and assign it to a new variable
        scaled_ghost_image = pygame.transform.scale(ghost_image, (TILE , TILE))

        # Get the rectangle of the image for positioning
        ghost_rect = scaled_ghost_image.get_rect()
        ghost_rect.center = (self.state.ghost.x*TILE+TILE//2, self.state.ghost.y*TILE+TILE//2) # Set the center of the rectangle to the ghost's position

        # Blit the ghost image onto the screen at the ghost's position
        self.screen.blit(scaled_ghost_image, ghost_rect)   
        
        # pygame.draw.circle(self.screen,RED,(self.state.ghost.x*TILE+TILE//2, self.state.ghost.y*TILE+TILE//2),TILE//2-2)
        
        
        # Score + messages
        if self.state.pac_on_dot():
            msg=f"WON! Score: {self.state.score} 🎉 (Esc exits)"
        elif self.state.pac_on_ghost():
            msg=f"LOST! Score: {self.state.score} (Esc exits)"
        else:
            msg=f"Score: {self.state.score}"        
        
        self.screen.blit(self.font.render(msg,True,WHITE),(5,5))
        self.screen.blit(self.font.render(self.msg_from_agent,True,WHITE),(5,TILE))
        pygame.display.flip()
