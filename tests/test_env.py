import unittest
from gymnasium.utils.env_checker import check_env
from tetris_gym.env import TetrisEnv

class TestTetrisEnv(unittest.TestCase):

    def test_gym_compliance(self):
        """
        Check if the environment is compliant with the Gymnasium API.
        """
        # It will raise an exception if it's not compliant
        env = TetrisEnv()
        check_env(env)
        env.close()
        print("Gymnasium compliance check passed.")

    def test_reset(self):
        """Test the reset method."""
        env = TetrisEnv()
        obs, info = env.reset()
        self.assertIn("board", obs)
        self.assertIn("next_piece", obs)
        self.assertIn("score", info)
        self.assertEqual(info['score'], 0)
        env.close()

    def test_step(self):
        """Test a single step in the environment."""
        env = TetrisEnv()
        env.reset()
        action = env.action_space.sample() # Take a random action
        obs, reward, terminated, truncated, info = env.step(action)

        self.assertIn("board", obs)
        self.assertIsInstance(reward, (int, float))
        self.assertIsInstance(terminated, bool)
        self.assertIsInstance(truncated, bool)
        self.assertIn("score", info)
        env.close()

if __name__ == '__main__':
    unittest.main()
