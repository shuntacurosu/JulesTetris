import pytest
from gymnasium.utils.env_checker import check_env
from tetris_gym.env import TetrisEnv

@pytest.fixture
def env():
    """Pytest fixture to provide a clean environment instance."""
    env = TetrisEnv()
    yield env
    env.close()

def test_gym_compliance(env):
    """
    Check if the environment is compliant with the Gymnasium API.
    It will raise an exception if it's not compliant.
    """
    check_env(env)

def test_reset(env):
    """Test the reset method."""
    obs, info = env.reset()
    assert "board" in obs
    assert "next_piece" in obs
    assert "score" in info
    assert info['score'] == 0

def test_step(env):
    """Test a single step in the environment."""
    env.reset()
    action = env.action_space.sample()  # Take a random action
    obs, reward, terminated, truncated, info = env.step(action)

    assert "board" in obs
    assert isinstance(reward, (int, float))
    assert isinstance(terminated, bool)
    assert isinstance(truncated, bool)
    assert "score" in info
