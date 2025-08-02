import random
import numpy as np
import torch
import torch.nn.functional as F
from collections import deque
from models import DQN


class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size

    def add(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def sample(self):
        batch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.tensor(np.array(states), dtype=torch.float32),
            torch.tensor(actions, dtype=torch.int64),
            torch.tensor(rewards, dtype=torch.float32),
            torch.tensor(np.array(next_states), dtype=torch.float32),
            torch.tensor(dones, dtype=torch.float32)
        )

    def __len__(self):
        return len(self.memory)


class DQNAgent:
    def __init__(self, state_size, action_size, device, lr=1e-3,
                 gamma=0.99, buffer_size=100000, batch_size=256, tau=1e-3, epsilon_start=1.0, epsilon_end=0.015, epsilon_decay=0.995):

        self.state_size = state_size
        self.action_size = action_size
        self.device = device

        self.qnetwork_local  = DQN(state_size, action_size, n_stack=3).to(device)
        self.qnetwork_target = DQN(state_size, action_size, n_stack=3).to(device)
        self.optimizer = torch.optim.Adam(self.qnetwork_local.parameters(), lr=lr)

        self.memory = ReplayBuffer(buffer_size, batch_size)
        self.batch_size = batch_size
        self.gamma = gamma
        self.tau = tau

        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay

    def step(self, state, action, reward, next_state, done):
        self.memory.add(state, action, reward, next_state, done)

        if len(self.memory) > self.batch_size:
            experiences = self.memory.sample()
            self.learn(experiences)

    def act(self, state):
        state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).to(self.device)
        if random.random() > self.epsilon:
            with torch.no_grad():
                q_values = self.qnetwork_local(state)
            return q_values.argmax().item()
        else:
            return random.choice(range(self.action_size))
        
    def get_action(self, state):
        """Selects action using the trained policy (no exploration)"""
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        self.qnetwork_local.eval()
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
        self.qnetwork_local.train()
        return np.argmax(action_values.cpu().data.numpy())

    def learn(self, experiences):
        states, actions, rewards, next_states, dones = experiences
        states, actions, rewards, next_states, dones = (
            states.to(self.device), actions.to(self.device), rewards.to(self.device),
            next_states.to(self.device), dones.to(self.device))

        # Compute Q targets
        with torch.no_grad():
            Q_targets_next = self.qnetwork_target(next_states).max(1)[0]
            Q_targets = rewards + (self.gamma * Q_targets_next * (1 - dones))

        Q_expected = self.qnetwork_local(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        loss = F.mse_loss(Q_expected, Q_targets)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.soft_update(self.qnetwork_local, self.qnetwork_target)

        

    def soft_update(self, local_model, target_model):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(self.tau * local_param.data + (1.0 - self.tau) * target_param.data)
