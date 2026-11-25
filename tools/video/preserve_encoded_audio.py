"""Keep an exact archived AAC track when a film changes only picture/caption timing."""

import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def packets(path, stream):
    return json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-select_streams', stream, '-show_packets',
        '-show_entries', 'packet=pts,dts,duration,size,data_hash',
        '-show_data_hash', 'sha256', '-of', 'json', str(path)]))['packets']


def preserve(movie, source, guide_path, source_sha256):
    assert digest(source) == source_sha256, 'Audio source does not match the reviewed movie'
    guide = json.loads(guide_path.read_text())
    before_sha = digest(movie)
    assert guide['sha256'] == before_sha, 'Guide does not identify the candidate'
    original_audio = packets(source, 'a:0')
    original_picture = packets(movie, 'v:0')
    assert original_audio and original_picture
    temporary = movie.with_suffix('.audio-preserved.mp4')
    assert not temporary.exists(), 'A prior audio-preservation attempt needs inspection'
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', str(movie), '-i', str(source),
                    '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart',
                    str(temporary)], check=True)
    assert packets(temporary, 'a:0') == original_audio, 'AAC packet bytes or timing changed'
    assert packets(temporary, 'v:0') == original_picture, 'Picture packet bytes or timing changed'
    temporary.replace(movie)
    guide['sha256'] = digest(movie)
    guide_path.write_text(json.dumps(guide, ensure_ascii=False, indent=2) + '\n')
    return {'source_movie_sha256': source_sha256, 'candidate_before_audio_copy_sha256': before_sha,
            'candidate_sha256': guide['sha256'], 'source_aac_packets': len(original_audio),
            'source_aac_packet_records_sha256': sha256(json.dumps(original_audio, sort_keys=True).encode()).hexdigest(),
            'candidate_picture_packets': len(original_picture), 'aac_bytes_and_timestamps_identical': True,
            'picture_bytes_and_timestamps_unchanged': True, 'new_audio_encoding': False}


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--movie', required=True, type=Path)
    cli.add_argument('--source', required=True, type=Path)
    cli.add_argument('--guide', required=True, type=Path)
    cli.add_argument('--source-sha256', required=True)
    args = cli.parse_args()
    print(json.dumps(preserve(args.movie, args.source, args.guide, args.source_sha256), indent=2))
