import gymnasium as gym
import tetris_gym # This registers the env, critical for gym.make to work
import keyboard
import time
import os

def main():
    """Main game loop for manual play."""
    try:
        # To use gym.make, the package needs to be installed via `pip install -e .`
        env = gym.make("tetris_gym:env/TetrisEnv-v0", render_mode='human')
        obs, info = env.reset()
        done = False

        fall_time = time.time()
        fall_speed = 0.5  # Time in seconds for a piece to drop one step

        # Debounce for rotation and movement to avoid overly sensitive controls
        last_input_time = 0
        input_cooldown = 0.12 # 120ms cooldown

        while not done:
            current_time = time.time()
            action = None

            # --- Handle Input with Cooldown ---
            if current_time - last_input_time > input_cooldown:
                if keyboard.is_pressed('q'):
                    print("Quitting game.")
                    break

                if keyboard.is_pressed('left') or keyboard.is_pressed('a'):
                    action = 1  # Move Left
                    last_input_time = current_time
                elif keyboard.is_pressed('right') or keyboard.is_pressed('d'):
                    action = 2  # Move Right
                    last_input_time = current_time
                elif keyboard.is_pressed('space'):
                    action = 6  # Hard Drop
                    last_input_time = current_time
                elif keyboard.is_pressed('up') or keyboard.is_pressed('w'):
                    action = 4  # Rotate CW
                    last_input_time = current_time

            # Soft drop is handled by the fall timer logic, no cooldown needed
            is_soft_dropping = keyboard.is_pressed('down') or keyboard.is_pressed('s')

            # --- Game Logic Step ---
            # If there's a user action, perform it immediately
            if action is not None:
                obs, reward, terminated, truncated, info = env.step(action)
                done = terminated or truncated
                if action == 6: # If hard drop, reset fall timer to spawn next piece faster
                    fall_time = time.time()

            # Check if it's time for the piece to fall automatically
            effective_fall_speed = 0.05 if is_soft_dropping else fall_speed
            if time.time() - fall_time > effective_fall_speed:
                # Action 3 is soft drop, which is the same as the piece falling one step
                obs, reward, terminated, truncated, info = env.step(3)
                done = terminated or truncated
                fall_time = time.time()

            time.sleep(0.02) # Prevents CPU hogging

    finally:
        if 'env' in locals():
            env.close()
        print("\n" + "="*20)
        print("   GAME OVER")
        if 'info' in locals() and info:
             print(f"  Final Score: {info.get('score', 0)}")
        print("="*20)


if __name__ == "__main__":
    if os.name == 'posix' and os.geteuid() != 0:
        print("WARNING: On Linux, the 'keyboard' library may need root permissions.")
        print("If you face issues, try running with 'sudo python play.py'.\n")

    print("Starting Tetris!")
    print("Make sure you have installed the game package by running:")
    print("pip install -e .")
    print("\n--- CONTROLS ---")
    print("A/D or Left/Right : Move")
    print("W or Up             : Rotate")
    print("S or Down           : Soft Drop")
    print("Space               : Hard Drop")
    print("Q                   : Quit")
    print("------------------\n")

    for i in range(3, 0, -1):
        print(f"Starting in {i}...")
        time.sleep(1)

    main()
