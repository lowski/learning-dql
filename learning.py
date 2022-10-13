from tf_agents.environments import tf_py_environment, utils
from tf_agents.utils import common

import scenes
from learning import dqn, training
from learning.environment import Environment
from learning.visualize import visualize_policy

LEARNING_RATE = 0.001
BATCH_SIZE = 64
ITERATIONS = 10000

REPLAY_BUFFER_LEN = 10000
COLLECT_STEPS_PER_ITERATION = 1
REPLAY_BUFFER_INITIAL_STEPS = 100

INTERVAL_LOG = 10
INTERVAL_EVAL = 30


def main():
    scene = scenes.simple_corridor

    print('Creating environments...')
    tf_train_env = tf_py_environment.TFPyEnvironment(Environment(scene, max_time=100))
    tf_eval_env = tf_py_environment.TFPyEnvironment(Environment(scene, max_time=100))

    print('Creating agent...')
    qnet = dqn.create_dqn(tf_train_env, [100, 50])
    agent = dqn.create_dqn_agent(tf_train_env, qnet, learning_rate=LEARNING_RATE)
    visualize_policy(scene, agent.policy)

    agent.train = common.function(agent.train)
    agent.train_step_counter.assign(0)

    rewards = []

    print('Creating replay buffer...')
    replay_buffer = training.create_replay_buffer(tf_train_env, agent, REPLAY_BUFFER_LEN)
    replay_buffer_observer = replay_buffer.add_batch
    replay_buffer_iterator = iter(replay_buffer.as_dataset(
        sample_batch_size=BATCH_SIZE,
        num_steps=2,
    ).prefetch(3))

    print('Populating replay buffer...')
    training.run_random_policy_tf_driver(tf_train_env, replay_buffer_observer,
                                         num_episodes=50)

    print('Running training loop...')
    driver = training.create_tf_driver(
        tf_train_env,
        agent.collect_policy,
        observer=replay_buffer_observer,
        num_episodes=2,
    )

    for _ in range(ITERATIONS):
        driver.run()

        experience, _ = next(replay_buffer_iterator)
        loss = agent.train(experience).loss

        step = agent.train_step_counter.numpy()

        if step % INTERVAL_LOG == 0:
            print('step = {} | loss = {}'.format(step, loss))

        if step % INTERVAL_EVAL == 0:
            reward = training.evaluate(tf_eval_env, agent.policy)
            print('step = {} | Average Reward = {}'.format(step, reward))
            rewards.append(reward)
            visualize_policy(scene, agent.policy)

    print(rewards)


if __name__ == '__main__':
    main()
