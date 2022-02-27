import os
import subprocess
from shutil import which
import pathlib

import pytest
import path

from jaraco import envs


env_types = pytest.mark.parametrize(
    "cls,create_opts",
    [
        (envs.VirtualEnv, ["--no-setuptools", "--no-pip", "--no-wheel"]),
        (envs._VEnv, ["--without-pip"]),
    ],
)


win37 = 'platform.system() == "Windows" and sys.version_info < (3, 8)'

path_types = pytest.mark.parametrize(
    "PathCls",
    [
        pytest.param(pathlib.Path, marks=pytest.mark.xfail(win37)),
        path.Path,
    ],
)


@env_types
@path_types
def test_root_pathlib(tmp_path, cls, create_opts, PathCls):
    venv = cls()
    vars(venv).update(root=PathCls(tmp_path), name=".venv", create_opts=create_opts)
    venv.ensure_env()

    possible_bin_dirs = (tmp_path / ".venv/bin", tmp_path / ".venv/Scripts")
    bin_dir = next(f for f in possible_bin_dirs if f.exists())
    expected_python = which("python", path=bin_dir)

    cmd = [venv.exe(), "-c", "import sys; print(sys.executable)"]
    out = subprocess.check_output(cmd, text=True).strip()
    assert os.path.samefile(out, expected_python)
