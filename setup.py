from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
build_exe_options = {"include_files" : [
    os.path.join(PYTHON_INSTALL_DIR, "DLLs", "libcrypto-1_1-x64.dll"),
    os.path.join(PYTHON_INSTALL_DIR, "DLLs", "libssl-1_1-x64.dll")]}

setup(
    name="TwiTracker",
    version="1.0",
    description="TwiTracker",
    executables=[Executable("main.py")]
)