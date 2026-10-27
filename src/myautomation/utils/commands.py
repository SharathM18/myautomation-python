import os
import subprocess
from pathlib import Path
from typing import Any


def execute_command(
    command_list: list[str], cwd: Path | None, env: dict[str, str] | None = None
) -> tuple[bool, Any]:
    """
    Executes a system command, streams its output live, and captures the final status.
    Returns a tuple: (Success Boolean, Error Message/Exception or None)
    """
    try:
        process_env = os.environ.copy()
        if env is not None:
            process_env.update(env)

        # Custom env variables can be added here
        # env["HTTP_PROXY"] = "http://127.0.0.1:8080"

        cwd_path = str(cwd) if cwd else None

        # Start the process in the background
        process = subprocess.Popen(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Redirects stderr into the stdout stream
            text=True,
            bufsize=1,
            env=process_env,
            cwd=cwd_path,  # Current Working Directory
        )

        # Stream stdout in real-time to the terminal line by line
        if process.stdout:
            for line in process.stdout:
                print(line, end="")

        # Wait for the command to fully finish execution
        process.wait()

        # Check the final exit status
        if process.returncode == 0:
            return True, None
        else:
            return False, f"Command failed with exit code {process.returncode}"

    except Exception as e:
        # Catch any structural errors (like file not found / command doesn't exist)
        return (
            False,
            f"System error while trying to run {command_list.join(' ')}: \n{str(e)}",
        )
