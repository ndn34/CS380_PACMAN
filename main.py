
import sys
import game
import agents

    
def main():
    g = game.Game()
    if (sys.argv[1] == 'human'):
        agent = agents.Human(g.state)
    elif (sys.argv[1] == 'random'):
        agent = agents.Random(g.state)
    elif (sys.argv[1] == 'qplayer'):
        agent = agents.QPlayer(g.state)
        episodes = None
        file_path = None
        if sys.argv[2] == 'learn':
            if len(sys.argv) > 3:
                episodes = int(sys.argv[3])
            if len(sys.argv) > 4:
                file_path = sys.argv[4]
            agent.learn_episodes(episodes, file_path)
        if sys.argv[2] == 'play':
            if len(sys.argv) == 4:
                file_path = sys.argv[3]
            agent.upload_q_table(file_path)
    else:
        print( "The agent is not defined in the systme!")
        exit()   
    g.play(agent)

if __name__=="__main__":
    main()