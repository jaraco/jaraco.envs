import os
import sys
import subprocess
import platform
import contextlib

from path import Path


class VirtualEnv:
    """
    >>> mp = getfixture('monkeypatch')
    >>> root = getfixture('tmp_path')
    >>> mp.setenv('SERVICES_ROOT', str(root))

    Subclass VirtualEnv and supply name and req:

    >>> class MyVirtualEnv(VirtualEnv):
    ...     name = '.venv'
    ...     req = 'example'
    >>> env = MyVirtualEnv().create()
    """

    root = Path(os.environ.get('SERVICES_ROOT', '.cache/services'))
    clean_opts = ["--no-setuptools", "--no-pip", "--no-wheel"]

    @property
    def dir(self):
        return self.root / self.name

    def create(self):
        self.ensure_env()
        self.install()
        return self

    def ensure_env(self):
        if os.path.exists(self.dir):
            return
        cmd = [sys.executable, '-m', 'virtualenv', self.dir]
        with contextlib.suppress(AttributeError):
            cmd += ['--python', self.python]
        with contextlib.suppress(AttributeError):
            cmd += self.create_opts
        subprocess.check_call(cmd)

    def install(self):
        cmd = [self.exe(), '-m', 'pip', 'install', self.req]
        env = os.environ.copy()
        env.update(getattr(self, 'install_env', {}))
        subprocess.check_call(cmd, env=env)

    def exe(self, cmd='python'):
        bin_or_scripts = 'Scripts' if platform.system() == 'Windows' else 'bin'
        return os.path.join(self.dir, bin_or_scripts, cmd)

    def env_vars(self):
        return {}


class VEnv(VirtualEnv):
    """
    venv-based version of VirtualEnv.
    """

    clean_opts = ["--without-pip"]

    def ensure_env(self):
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

    def ensure_env(self):
        pass

    def install(self):
        cmd = [sys.executable, '-m', 'tox', '-e', self.name, '--notest']
        subprocess.check_call(cmd)
