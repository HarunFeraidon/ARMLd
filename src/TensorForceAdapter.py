
from collections import namedtuple

import PongRivanna as env

from tensorforce.environments import Environment as force_env

StateTerminalReward = namedtuple('StateReward', ['state','terminal', 'reward'])

class adapter(force_env):
    def __init__(self, game):
        self.game = game

    def execute(self, actions):
        #print(self.game.ret.state, actions)
        ret = self.game.simple_step(actions)
        self.game.draw()
        return StateTerminalReward(ret.state, ret.done, ret.reward)

    def reset(self):
        return self.game.reset()

    def __str__(self):
        return 'PongRivanna'

    @property
    def states(self):
        return dict(shape=self.game.flat().shape, type='float32')

    @property
    def actions(self):
        return dict(num_actions=len(self.game.DIRECTIONS), type='int')

class real_adapter(adapter):
    def execute(self, actions):
        ret = self.game.step(actions)
        self.game.draw()
        return StateTerminalReward(ret.state, ret.done, ret.reward)

    def __str__(self):
        return 'PongRivanna-RealValued'

    @property
    def actions(self):
        return dict(
            shape=(2,),
            min_value=-1*env.speed,
            max_value=env.speed,
            type='float32'
        )


default_environment = adapter(env)
