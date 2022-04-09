import os
import os.path as osp
import subprocess

import schedule
from rich.console import Console

CONSOLE = Console()

# https://schedule.readthedocs.io/en/stable/examples.html


def pose_feasibility(cat, out_dir='mmaction2/data/phar/pose'):
    """Schedule for the pose_feasibility.py script."""
    CONSOLE.print(f'Checking pose feasibility for {cat}...', style='green')
    script_path = 'tools/analysis/pose_feasibility.py'

    subargs = ['python', script_path, cat, '--out-dir', out_dir, '--resume']
    subprocess.run(subargs)
    return schedule.CancelJob


def extract_audio(in_dir, out_dir):
    """Scheduler to extract audio from videos_val.

    Args:
        in_dir (_type_): _description_
        out_dir (_type_): _description_

    Returns:
        _type_: _description_
    """
    import time
    script_dir = '/mmaction2/tools/data/extract_audio.py'
    for dIr in os.listdir(in_dir):
        CONSOLE.print(f'Extracting videos for {dIr}...', style='green')
        CONSOLE.print(osp.join(in_dir, dIr))
        CONSOLE.print(osp.join(out_dir, dIr))

        subargs = [
            'python', script_dir,
            osp.join(in_dir, dIr),
            osp.join(out_dir, dIr), '--level', '1', '--ext', 'avi'
        ]
        subprocess.run(subargs)
        time.sleep(30)
    return schedule.CancelJob


def extract_audio_feature(in_dir, out_dir):
    """Extract spectogram features from audio.

    Args:
        in_dir (_type_): _description_
        out_dir (_type_): _description_

    Returns:
        _type_: _description_
    """
    script_dir = '/mmaction2/tools/data/build_audio_features.py'
    for dIr in os.listdir(in_dir):
        dir_path = osp.join(in_dir, dIr)
        for audio in os.listdir(dir_path):
            audio_path = osp.join(dir_path, audio)
            subargs = [
                'python', script_dir, audio_path,
                osp.join(out_dir,
                         audio.split('.')[0] + '.npy'), '--level', '1',
                '--ext', 'avi'
            ]
            subprocess.run(subargs)

    return schedule.CancelJob


# schedule.every().sunday.at('22:43').do(extract_audio,
#                                        in_dir='data/ucf101/videos/',
#                                        out_dir='data/ucf101/audio/')

schedule.every().thursday.at('05:00').do(
    pose_feasibility, cat='doggy', out_dir='mmaction2/data/phar/pose/0.4_0.4/')

while True:
    schedule.run_pending()
