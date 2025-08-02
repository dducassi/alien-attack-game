import torch
import numpy as np
from dqn_agent import DQNAgent
from rcenv import RaidCanopusEnv
from raid_canopus import RaidCanopus
from collections import deque
import os

def train():
    # Initialize environment and agent
    game = RaidCanopus()
    env = RaidCanopusEnv(game)
    game.env = env  
    state_size = env.observation_size
    N = 3
    action_size = env.action_size
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    agent = DQNAgent(state_size, action_size, device)
    # Load previously saved model if it exists
    if os.path.exists("dqn_final.pth"):
        agent.qnetwork_local.load_state_dict(torch.load("dqn_final.pth", map_location=device))
        agent.qnetwork_target.load_state_dict(torch.load("dqn_final.pth", map_location=device))
        print("[INFO] Loaded previous model from dqn_final.pth")
    else:
        print("[INFO] No saved model found. Starting fresh.")

    if os.path.exists("epsilon.npy"):
        agent.epsilon = float(np.load("epsilon.npy"))
        print(f"[INFO] Resuming with epsilon: {agent.epsilon}")
    #agent.epsilon = 0.1
    print(f"[DEBUG] Initial epsilon: {agent.epsilon}")

    episodes = 2500
    max_t = 36000
    try:
        for i_episode in range(1, episodes+1):
            obs = env.reset()                 # shape (D,)
            buf = deque([obs.copy()]*N, maxlen=N)
            state = np.concatenate(buf)       # shape (N*D,)
            total_reward = 0

            for t in range(max_t):
                action = agent.act(state)    # now expects N*D input
                next_obs, reward, done, _ = env.step(action)
                buf.append(next_obs.copy())  # drop the oldest, add the newest

                next_state = np.concatenate(buf)  # new N*D vector
                agent.step(state, action, reward, next_state, done)

                state = next_state
                total_reward += reward
                if done:
                    break
            
            agent.epsilon = max(agent.epsilon_end, agent.epsilon * agent.epsilon_decay)

            print(f"Episode {i_episode} Total Reward: {total_reward:.2f} Epsilon: {agent.epsilon:.3f}")

            # Save model
            if i_episode % 50 == 0:
                torch.save(agent.qnetwork_local.state_dict(), f"checkpoint_{i_episode}.pth")
    except KeyboardInterrupt:
        print("\nTraining interrupted by user.")
    
    finally:
        torch.save(agent.qnetwork_local.state_dict(), "dqn_final.pth")
        print("Final model saved.")
        np.save("epsilon.npy", agent.epsilon)

        

if __name__ == "__main__":
    train()
