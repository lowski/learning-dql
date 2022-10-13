from time import sleep

from tf_agents.environments import tf_py_environment

from learning import training
from learning.environment import Environment
from learning.scene import Scene


def visualize_policy(scene: Scene, policy):
    env = Environment(scene, True)
    tf_env = tf_py_environment.TFPyEnvironment(env)

    driver = training.create_tf_driver(
        tf_env,
        policy,
        observer=lambda x: None,
        num_episodes=1,
    )

    driver.run()
    sleep(2)
    env.destroy()
