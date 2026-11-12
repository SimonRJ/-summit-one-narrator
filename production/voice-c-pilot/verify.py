import json,subprocess
from pathlib import Path
p=Path('build/amc2025-q17')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p/'final.mp4')]))
assert len([s for s in probe['streams'] if s['codec_type']=='audio'])==1
qa=json.loads((p/'qa.json').read_text());timing=json.loads((p/'timing.json').read_text())
assert timing['old_audio_used'] is False
qa.update(old_narration_removed=True,audio_stream_count=1,voice_reference_sha256=timing['reference_sha256'],voice_source='approved synthetic voice C',exact_reference_voice_match=False)
(p/'qa.json').write_text(json.dumps(qa,indent=2))
print(json.dumps(qa))
