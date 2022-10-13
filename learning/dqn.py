from typing import List

import tensorflow as tf
from tf_agents.agents.dqn import dqn_agent

from tf_agents.environments import py_environment, TFPyEnvironment, PyEnvironment
from tf_agents.networks import sequential, network
from tf_agents.specs import tensor_spec


# Define a helper function to create Dense layers configured with the right
# activation and kernel initializer.
from tf_agents.utils import common


def _create_dense_layer(num_units):
    return tf.keras.layers.Dense(
        num_units,
        activation=tf.keras.activations.relu,
        kernel_initializer=tf.keras.initializers.VarianceScaling(
            scale=2.0, mode='fan_in', distribution='truncated_normal'))


def create_dqn(env: PyEnvironment, layer_shapes: List[int]):
    action_tensor_spec = tensor_spec.from_spec(env.action_spec())
    num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1

    layers = [_create_dense_layer(shape) for shape in layer_shapes]
    output_layer = tf.keras.layers.Dense(
            num_actions,
            activation=None,
            kernel_initializer=tf.keras.initializers.RandomUniform(minval=-0.03, maxval=0.03),
            bias_initializer=tf.keras.initializers.Constant(-0.2)
        )

    return sequential.Sequential(layers + [output_layer])


def create_dqn_agent(env: TFPyEnvironment, q_network: network.Network, learning_rate=0.01):
    # optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    optimizer = tf.compat.v1.train.AdamOptimizer(learning_rate)
    train_step_counter = tf.Variable(0)

    agent = dqn_agent.DqnAgent(
        time_step_spec=env.time_step_spec(),
        action_spec=env.action_spec(),
        q_network=q_network,
        optimizer=optimizer,
        td_errors_loss_fn=common.element_wise_squared_loss,
        train_step_counter=train_step_counter
    )
    # agent.initialize()

    return agent
