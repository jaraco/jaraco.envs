from __future__ import annotations

import contextlib
import os
import platform
import subprocess
import sys
from typing import TYPE_CHECKING, Any

from path import Path

if TYPE_CHECKING:
    from _typeshed import StrPath
    from typing_extensions import Self


class VirtualEnv:
    """
    >>> mp = getfixture('monkeypatch')
    >>> root = getfixture('tmp_path')
    >>> mp.setenv('SERVICES_ROOT', str(root))

    Subclass VirtualEnv and supply req:

    >>> class MyVirtualEnv(VirtualEnv):
    ...     req = 'example'
    >>> env = MyVirtualEnv().create()
    """

    root = Path(os.environ.get('SERVICES_ROOT', '.cache/services'))
    clean_opts = ["--no-setuptools", "--no-pip", "--no-wheel"]
    name = '.venv'
    if TYPE_CHECKING:
        # Don't actually define these. Let method calls fail with AttributeError
        python: str
        create_opts: list[str]
        req: str

    @property
    def dir(self) -> Path:
        return self.root / self.name

    def create(self) -> Self:
        self.ensure_env()
        self.install()
        return self

    def ensure_env(self) -> None:
        if os.path.exists(self.dir):
            return
        cmd: list[StrPath] = [sys.executable, '-m', 'virtualenv', self.dir]
        with contextlib.suppress(AttributeError):
            cmd += ['--python', self.python]
        with contextlib.suppress(AttributeError):
            cmd += self.create_opts
        subprocess.check_call(cmd)

    def install(self) -> None:
        cmd = [self.exe(), '-m', 'pip', 'install', self.req]
        env = os.environ.copy()
        env.update(getattr(self, 'install_env', {}))
        subprocess.check_call(cmd, env=env)

    def exe(self, cmd: StrPath = 'python') -> str:
        bin_or_scripts = 'Scripts' if platform.system() == 'Windows' else 'bin'
        return os.path.join(self.dir, bin_or_scripts, cmd)

    def env_vars(self) -> dict[Any, Any]:  # Always an empty dict, can be used anywhere.
        return {}


class VEnv(VirtualEnv):
    """
    venv-based version of VirtualEnv.
    """

    clean_opts = ["--without-pip"]

    def ensure_env(self) -> None:
        executable = getattr(self, 'python', sys.executable)
        cmd = [executable, '-m', 'venv', self.dir]
        with contextlib.suppress(AttributeError):
            cmd += ['--python', self.python]
        with contextlib.suppress(AttributeError):
            cmd += self.create_opts
        subprocess.check_call(cmd)


class ToxEnv(VirtualEnv):
    """
    A version of VirtualEnv that relies on tox to define and
    build environments.
    """

    root = Path('.tox')

    def ensure_env(self) -> None:
        pass

    def install(self) -> None:
        cmd = [sys.executable, '-m', 'tox', '-e', self.name, '--notest']
        subprocess.check_call(cmd)
