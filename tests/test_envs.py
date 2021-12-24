import subprocess
from shutil import which

import pytest

from jaraco import envs


@pytest.mark.parametrize(
    "cls,create_opts",
    [
        (envs.VirtualEnv, ["--no-setuptools", "--no-pip", "--no-wheel"]),
        (envs._VEnv, ["--without-pip"]),
    ],
)
def test_ensure_env(tmp_path, cls, create_opts):
    venv = cls()
    vars(venv).update(root=tmp_path, name=".venv", create_opts=create_opts)
    venv.ensure_env()

    possible_bin_dirs = (tmp_path / ".venv/bin", tmp_path / ".venv/Scripts")
    bin_dir = next(f for f in possible_bin_dirs if f.exists())
    expected_python = which("python", path=str(bin_dir))

    cmd = [venv.exe(), "-c", "import sys; print(sys.executable)"]
    out = str(subprocess.check_output(cmd).strip(), "utf-8")
    assert out == expected_python
