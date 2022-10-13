from tf_agents.environments import tf_py_environment, utils
from tf_agents.utils import common

import scenes
from learning import dqn, training
from learning.environment import Environment

LEARNING_RATE = 0.001
BATCH_SIZE = 64
ITERATIONS = 10000

REPLAY_BUFFER_LEN = 10000
COLLECT_STEPS_PER_ITERATION = 1
REPLAY_BUFFER_INITIAL_STEPS = 100

INTERVAL_LOG = 200
INTERVAL_EVAL = 1000


def main():
    print('Validating environment...')
    scene = scenes.simple_corridor
    utils.validate_py_environment(Environment(scene), episodes=5)

    print('Creating environments...')
    tf_train_env = tf_py_environment.TFPyEnvironment(Environment(scene))
    tf_eval_env = tf_py_environment.TFPyEnvironment(Environment(scene))

    print('Creating agent...')
    qnet = dqn.create_dqn(tf_train_env, [100, 50])
    agent = dqn.create_dqn_agent(tf_train_env, qnet, learning_rate=LEARNING_RATE)

    agent.train = common.function(agent.train)
    agent.train_step_counter.assign(0)

    rewards = []

    print('Evaluating agent pre training...')
    reward_pre_training = training.evaluate(tf_eval_env, agent.policy)
    rewards.append(reward_pre_training)

    print('Creating replay buffer...')
    replay_buffer = training.create_replay_buffer(tf_train_env, agent, REPLAY_BUFFER_LEN)
    replay_buffer_observer = replay_buffer.add_batch
    replay_buffer_iterator = iter(replay_buffer.as_dataset(
        sample_batch_size=1,
        num_steps=2,
    ).prefetch(3))

    print('Populating replay buffer...')
    training.run_random_policy_tf_driver(tf_train_env, replay_buffer_observer, REPLAY_BUFFER_INITIAL_STEPS)

    driver = training.create_tf_driver(
        tf_train_env,
        agent.collect_policy,
        observer=replay_buffer_observer,
        steps_per_iteration=COLLECT_STEPS_PER_ITERATION,
    )

    print('Running training loop...')
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

    print(rewards)


if __name__ == '__main__':
    main()
