from calculator.environment import Environment
from calculator.evaluator import evaluate
from calculator.parser import parse


def ev(text, env=None):
    """Parse and evaluate an expression string."""
    return evaluate(parse(text), env if env is not None else Environment())


def deg_env():
    env = Environment()
    env.set_angle_mode("deg")
    return env
