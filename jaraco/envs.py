from __future__ import unicode_literals

import os
import sys
import subprocess
import platform

import contextlib2

from path import Path


__metaclass__ = type


class VirtualEnv:
    root = Path(os.environ.get('SERVICES_ROOT', '.cache/services'))

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
        cmd = [
            sys.executable,
            '-m', 'virtualenv',
            self.dir,
        ]
        with contextlib2.suppress(AttributeError):
            cmd += ['--python', self.python]
        subprocess.check_call(cmd)

    def install(self):
        cmd = [
            self.exe(),
            '-m', 'pip',
            'install',
            self.req,
        ]
        env = os.environ.copy()
        env.update(getattr(self, 'install_env', {}))
        subprocess.check_call(cmd, env=env)

    def exe(self, cmd='python'):
        bin_or_scripts = 'Scripts' if platform.system() == 'Windows' else 'bin'
        return os.path.join(self.dir, bin_or_scripts, cmd)

    def env_vars(self):
        return {}


class _VEnv(VirtualEnv):
    """
    Experimental version of VirtualEnv, requires target environment
    to be Python 3.
    """
    def ensure_env(self):
        executable = getattr(self, 'python', sys.executable)
        cmd = [
            executable,
            '-m', 'venv',
            self.dir,
        ]
        subprocess.check_call(cmd)


class ToxEnv(VirtualEnv):
    """
    A version of VirtualEnv that relies on tox (and tox-venv)
    to define and build environments.
    """
    root = Path('.tox')

    def ensure_env(self):
        pass

    def install(self):
        cmd = [sys.executable, '-m', 'tox', '-e', self.name, '--notest']
        subprocess.check_call(cmd)
