from typing import Callable

from tf_agents import policies
from tf_agents.agents.dqn import dqn_agent
from tf_agents.drivers import py_driver, dynamic_step_driver, dynamic_episode_driver
from tf_agents.environments import py_environment, TFEnvironment, tf_py_environment
from tf_agents.policies import py_tf_eager_policy, random_tf_policy, TFPolicy
from tf_agents.replay_buffers import tf_uniform_replay_buffer


def evaluate(env: TFEnvironment, policy: policies.TFPolicy, episodes=10):
    """
    Evaluate a policy in a given environment for multiple episodes

    :return: average reward per episode
    """
    rewards = [0 for _ in range(episodes)]
    for i in range(episodes):
        ts = env.reset()
        reward = 0
        while not ts.is_last():
            step = policy.action(ts)
            ts = env.step(step)
            reward += ts.reward
        rewards[i] = reward
    return sum(rewards) / episodes


def create_py_driver(env: py_environment.PyEnvironment, policy, observer,
                     collect_steps_per_iteration) -> py_driver.PyDriver:
    """
    Create a driver for a TFEnvironment. Uses a PyDriver which will stop after a specified amount of max steps.
    """
    return py_driver.PyDriver(
        env,
        py_tf_eager_policy.PyTFEagerPolicy(
            policy, use_tf_function=True),
        [observer],
        max_steps=collect_steps_per_iteration)


def create_tf_driver(env: TFEnvironment, policy: TFPolicy, observer: Callable,
                     num_steps=None, num_episodes=None):
    """
    Create a driver for a TFEnvironment. Uses a DynamicStepDriver which will stop after a specified amount of max steps.
    """
    assert num_steps is not None or num_episodes is not None

    if num_episodes is not None:
        return dynamic_episode_driver.DynamicEpisodeDriver(
            env,
            policy,
            observers=[observer],
            num_episodes=num_episodes,
        )
    else:
        return dynamic_step_driver.DynamicStepDriver(
            env,
            policy,
            observers=[observer],
            num_steps=num_steps,
        )


def run_random_policy_py_driver(env: py_environment.PyEnvironment, observer, steps):
    tf_env = tf_py_environment.TFPyEnvironment(env)
    _random_policy = random_tf_policy.RandomTFPolicy(tf_env.time_step_spec(),
                                                     tf_env.action_spec())

    create_py_driver(
        env,
        py_tf_eager_policy.PyTFEagerPolicy(
            _random_policy, use_tf_function=True),
        observer,
        steps,
    ).run(env.reset())


def run_random_policy_tf_driver(env: TFEnvironment, observer, num_steps=None, num_episodes=None):
    create_tf_driver(
        env,
        get_random_policy(env),
        observer,
        num_steps=num_steps,
        num_episodes=num_episodes,
    ).run()


def get_random_policy(env: TFEnvironment):
    return random_tf_policy.RandomTFPolicy(
            env.time_step_spec(),
            env.action_spec())


def create_replay_buffer(env: TFEnvironment, agent: dqn_agent.DqnAgent, max_length=10000):
    return tf_uniform_replay_buffer.TFUniformReplayBuffer(
        agent.collect_data_spec,
        batch_size=env.batch_size,
        max_length=max_length)
