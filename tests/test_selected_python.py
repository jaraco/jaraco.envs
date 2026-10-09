import pathlib
import subprocess
import sys

from jaraco import envs


def test_venv_with_selected_python(tmp_path: pathlib.Path) -> None:
    class SelectedPython(envs.VEnv):
        python = sys.executable
        root = tmp_path
        create_opts = ['--without-pip']

    env = SelectedPython()
    env.ensure_env()
    assert (env.dir / 'pyvenv.cfg').is_file()
    output = subprocess.check_output(
        [env.exe(), '-c', 'print("selected interpreter works")'],
        text=True,
        encoding='utf-8',
    )
    assert output.strip() == 'selected interpreter works'
