import os
import sys
import subprocess
from shutil import which
import pathlib

import pytest
import path

from jaraco import envs


env_types = pytest.mark.parametrize("VEnvCls", [envs.VirtualEnv, envs.VEnv])

win37 = 'platform.system() == "Windows" and sys.version_info < (3, 8)'

path_types = pytest.mark.parametrize(
    "PathCls",
    [
        pytest.param(pathlib.Path, marks=pytest.mark.xfail(win37)),
        path.Path,
    ],
)


maybe_fspath = os.fspath if sys.version_info < (3, 8) else lambda x: x


@env_types
@path_types
def test_root_pathlib(tmp_path, VEnvCls, PathCls):
    venv = VEnvCls()
    vars(venv).update(
        root=PathCls(tmp_path), name=".venv", create_opts=VEnvCls.clean_opts
    )
    venv.ensure_env()

    possible_bin_dirs = (tmp_path / ".venv/bin", tmp_path / ".venv/Scripts")
    bin_dir = next(f for f in possible_bin_dirs if f.exists())
    expected_python = which("python", path=maybe_fspath(bin_dir))

    cmd = [venv.exe(), "-c", "import sys; print(sys.executable)"]
    out = subprocess.check_output(cmd, text=True, encoding='utf-8').strip()
    assert os.path.samefile(out, expected_python)
