"""Set up the lesson renderer on Linux Actions runners without a system package mirror."""
import base64
import hashlib
import io
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
from urllib.request import urlopen


def pip(*packages):
    subprocess.run([sys.executable, '-m', 'pip', 'install', '--disable-pip-version-check', *packages], check=True)


def install():
    target = Path(os.environ['RUNNER_TEMP']) / 'summit-media-tools'
    target.mkdir(parents=True, exist_ok=True)
    pip('pillow')
    if shutil.which('ffmpeg') is None:
        pip('imageio-ffmpeg==0.6.0')
        import imageio_ffmpeg
        executable = target / 'ffmpeg'
        if not executable.exists():
            executable.symlink_to(imageio_ffmpeg.get_ffmpeg_exe())
    if shutil.which('ffprobe') is None:
        if platform.system() != 'Linux' or platform.machine() not in ('x86_64', 'amd64'):
            raise RuntimeError('The pinned ffprobe distribution requires an x86-64 Linux runner')
        package = 'https://registry.npmjs.org/@ffprobe-installer/linux-x64/-/linux-x64-5.2.0.tgz'
        digest = 'D3UeqTLYPNs7pBWPLUYGehPdRVqU8eACox4OZy3pZUZatxye2YKlvBwEfaLdL1v2Z4FOAlLUhms0kY8m8kqSRA=='
        with urlopen(package, timeout=60) as response:
            payload = response.read()
        if hashlib.sha512(payload).digest() != base64.b64decode(digest):
            raise ValueError('The ffprobe distribution checksum differs from the pinned value')
        with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
            binary = archive.extractfile('package/ffprobe')
            if binary is None:
                raise ValueError('The ffprobe distribution contains no executable')
            executable = target / 'ffprobe'
            with executable.open('wb') as out:
                shutil.copyfileobj(binary, out)
            executable.chmod(0o755)
    from PIL import ImageFont
    try:
        for face in ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf'):
            ImageFont.truetype(face, 32)
    except OSError:
        pip('matplotlib')
        import matplotlib
        fonts = target / 'share/fonts'
        fonts.mkdir(parents=True, exist_ok=True)
        for name in ('DejaVuSans.ttf', 'DejaVuSans-Bold.ttf'):
            shutil.copy(Path(matplotlib.get_data_path()) / 'fonts/ttf' / name, fonts / name)
        data_dirs = str(target / 'share') + ':' + os.environ.get('XDG_DATA_DIRS', '/usr/local/share:/usr/share')
        with Path(os.environ['GITHUB_ENV']).open('a') as out:
            print('XDG_DATA_DIRS=' + data_dirs, file=out)
        os.environ['XDG_DATA_DIRS'] = data_dirs
        ImageFont.truetype('DejaVuSans.ttf', 32)
        ImageFont.truetype('DejaVuSans-Bold.ttf', 32)
    with Path(os.environ['GITHUB_PATH']).open('a') as out:
        print(target, file=out)
    for command in ('ffmpeg', 'ffprobe'):
        executable = shutil.which(command, path=str(target) + os.pathsep + os.environ['PATH'])
        subprocess.run([executable, '-version'], stdout=subprocess.DEVNULL, check=True)


if __name__ == '__main__':
    install()
