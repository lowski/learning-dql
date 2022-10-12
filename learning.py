from tf_agents.environments import utils

from learning.environment import Environment


def main():
    environment = Environment()
    utils.validate_py_environment(environment, episodes=5)


if __name__ == '__main__':
    main()
