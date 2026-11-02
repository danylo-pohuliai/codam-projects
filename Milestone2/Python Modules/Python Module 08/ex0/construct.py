import sys
import site
import os

if __name__ == "__main__":
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix')
                                       and sys.base_prefix != sys.prefix):
        m_stat = "Welcome to the construct"
        v_env = sys.prefix
        v_env_name = os.path.basename(v_env)
        inside = True
    else:
        m_stat = "You're still plugged in"
        v_env = "None detected"
        inside = False
    python_path = sys.executable
    print(f"\nMATRIX STATUS: {m_stat}\n")
    print(f"Current Python: {python_path}")
    if inside:
        print(f"Virtual Environment: {v_env_name}")
        print(f"Environment Path: {v_env}")
        print("\nSUCCESS: You're in an isolated environment!")
        print("Safe to install packages without affecting")
        print("the global system.\n")
        print(f"Package installation path:\n{site.getsitepackages()[0]}")
    else:
        print(f"Virtual Environment: {v_env}\n")
        print("WARNING: You're in the global environment!")
        print("The machines can see everything you install.\n")
        print("To enter the construct, run:\npython -m venv matrix_env")
        print("source matrix_env/bin/activate # On Unix")
        print("matrix_env\\Scripts\\activate # On Windows\n")
        print("Then run this program again.")
