import random
import math
from constants import *


class FiniteStateMachine(object):
    """
    A finite state machine.
    """
    def __init__(self, state):
        self.state = state

    def change_state(self, new_state):
        self.state = new_state

    def update(self, agent):
        self.state.check_transition(agent, self)
        self.state.execute(agent)


class State(object):
    """
    Abstract state class.
    """
    def __init__(self, state_name):
        """
        Creates a state.

        :param state_name: the name of the state.
        :type state_name: str
        """
        self.state_name = state_name

    def check_transition(self, agent, fsm):
        """
        Checks conditions and execute a state transition if needed.

        :param agent: the agent where this state is being executed on.
        :param fsm: finite state machine associated to this state.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")

    def execute(self, agent):
        """
        Executes the state logic.

        :param agent: the agent where this state is being executed on.
        """
        raise NotImplementedError("This method is abstract and must be implemented in derived classes")


class MoveForwardState(State):
    def __init__(self):
        super().__init__("MoveForward")
        self.actual_time = 0

    def check_transition(self, agent, state_machine):

        if self.actual_time > MOVE_FORWARD_TIME:
            state_machine.change_state(MoveInSpiralState())

        if agent.get_bumper_state():
            state_machine.change_state(GoBackState())

    def execute(self, agent):
        agent.set_velocity(FORWARD_SPEED, 0)
        self.actual_time += SAMPLE_TIME


class MoveInSpiralState(State):

    def __init__(self):
        super().__init__("MoveInSpiral")
        self.actual_time = 0

    def check_transition(self, agent, state_machine):
        if self.actual_time > MOVE_IN_SPIRAL_TIME:
            state_machine.change_state(MoveForwardState())

        if agent.get_bumper_state():
            state_machine.change_state(GoBackState())

    def execute(self, agent):
        agent.set_velocity(FORWARD_SPEED, FORWARD_SPEED/(INITIAL_RADIUS_SPIRAL + SPIRAL_FACTOR * self.actual_time))
        self.actual_time += SAMPLE_TIME


class GoBackState(State):
    def __init__(self):
        super().__init__("GoBack")
        self.actual_time = 0

    def check_transition(self, agent, state_machine):
        if self.actual_time > GO_BACK_TIME:
            state_machine.change_state(RotateState())

    def execute(self, agent):
        agent.set_velocity(BACKWARD_SPEED, 0)
        self.actual_time += SAMPLE_TIME


class RotateState(State):
    def __init__(self):
        super().__init__("Rotate")
        self.actual_time = 0
        self.go_front = False
        self.rand_direction = random.choice([-1, 1])
        self.rang_angle = random.uniform(-3.14, 3.14)

    def check_transition(self, agent, state_machine):
        if self.go_front:
            state_machine.change_state(MoveForwardState())
    
    def execute(self, agent):
        agent.set_velocity(0, self.rand_direction)
        self.actual_time += SAMPLE_TIME
        if self.actual_time > math.fabs(self.rang_angle):
            self.go_front = True
