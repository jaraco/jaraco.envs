import os
import subprocess
from shutil import which
import pathlib

import pytest
import path

from jaraco import envs


env_types = pytest.mark.parametrize("VEnvCls", [envs.VirtualEnv, envs.VEnv])
path_types = pytest.mark.parametrize("PathCls", [pathlib.Path, path.Path])


@env_types
@path_types
def test_root_pathlib(tmp_path, VEnvCls, PathCls):
    venv = VEnvCls()
    vars(venv).update(root=PathCls(tmp_path), create_opts=VEnvCls.clean_opts)
    venv.ensure_env()

    possible_bin_dirs = (tmp_path / ".venv/bin", tmp_path / ".venv/Scripts")
    bin_dir = next(f for f in possible_bin_dirs if f.exists())
    expected_python = which("python", path=bin_dir)

    cmd = [venv.exe(), "-c", "import sys; print(sys.executable)"]
    out = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
    assert os.path.samefile(out, expected_python)
