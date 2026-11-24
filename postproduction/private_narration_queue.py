"""Transport a single private narration take without printing the text or recording."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = Path(__file__).resolve().parents[1]
MODEL_REVISION = '7936080b41163874f38610f46f438e2c0757f9fd'
REFERENCE = '0f3304a393ee504e9fa22537267ac03f150569a5fab0859616f261d009513362'


def database(params, update=None):
    base = os.environ['SUPABASE_URL'].rstrip('/')
    token = os.environ['SUPABASE_SERVICE_ROLE_KEY']
    headers = {'apikey': token, 'Authorization': 'Bearer '+token, 'Content-Type': 'application/json'}
    if update is not None:
        headers['Prefer'] = 'return=minimal'
    url = base+'/rest/v1/protected_narration_work?'+urllib.parse.urlencode(params)
    data = None if update is None else json.dumps(update).encode()
    request = urllib.request.Request(url,data=data,method='GET' if update is None else 'PATCH',headers=headers)
    try:
        with urllib.request.urlopen(request,timeout=90) as response:
            payload = response.read()
    except urllib.error.HTTPError as error:
        raise SystemExit('Private transfer returned HTTP '+str(error.code)) from None
    return json.loads(payload) if payload else None


def run(action):
    raw_batch = os.environ.get('BATCH_ID', '')
    if not raw_batch and action == 'list' and os.environ.get('GITHUB_EVENT_NAME') == 'push':
        request = json.loads((ROOT/'production/private-narration-request.json').read_text())
        if set(request) != {'batch_id'}:
            raise SystemExit('Invalid private batch request.')
        raw_batch = request['batch_id']
    batch = str(uuid.UUID(raw_batch))
    if raw_batch != batch:
        raise SystemExit('Invalid private batch identifier.')
    where = {'batch_id':'eq.'+batch}
    if action == 'list':
        rows = database({**where,'select':'slot','audio_sha256':'is.null','order':'slot.asc'})
        slots = [r['slot'] for r in rows]
        if len(slots)>32 or any(type(i) is not int or not 1<=i<=32 for i in slots):
            raise SystemExit('Invalid batch rows.')
        with open(os.environ['GITHUB_OUTPUT'],'a') as output:
            print('batch='+batch, file=output)
            print('slots='+json.dumps(slots), file=output)
        return
    slot = int(os.environ['SLOT'])
    if not 1<=slot<=32: raise SystemExit('Invalid batch slot.')
    where['slot']='eq.'+str(slot)
    rows=database({**where,'select':'scene_number,narration,narration_sha256,audio_sha256'})
    if len(rows)!=1: raise SystemExit('Missing private work item.')
    row=rows[0]
    text=row['narration']
    scene=row['scene_number']
    if not 1<=scene<=32 or hashlib.sha256(text.encode()).hexdigest()!=row['narration_sha256']:
        raise SystemExit('Private source did not verify.')
    if action=='fetch':
        scenes=[{} for _ in range(scene-1)]+[{'narration':text}]
        (ROOT/'production/scripts/PRIVATE.json').write_text(json.dumps({'scenes':scenes}))
        (Path(os.environ['RUNNER_TEMP'])/'narration-scene').write_text(str(scene))
    elif action=='store':
        stem=ROOT/'build/t01-studio'/f'PRIVATE-{scene:02}'
        info=json.loads(stem.with_suffix('.json').read_text())
        if not (info.get('narration_sha256')==row['narration_sha256'] and info.get('model_revision')==MODEL_REVISION
                and info.get('reference_sha256')==REFERENCE and info.get('natural_speed') is True):
            raise SystemExit('The recording did not match its approved inputs.')
        audio=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(stem.with_suffix('.wav')),
            '-map','0:a:0','-c:a','flac','-f','flac','pipe:1'])
        checksum=hashlib.sha256(audio).hexdigest()
        if row['audio_sha256'] is None:
            database({**where,'audio_sha256':'is.null'},{'audio_flac':'\\x'+audio.hex(),
                'audio_sha256':checksum,'voice_evidence':info})
        receipt=database({**where,'select':'audio_sha256'})
        if len(receipt)!=1 or not receipt[0]['audio_sha256']:
            raise SystemExit('Private receipt missing.')
        # A concurrent run can finish first. Its immutable take receives editorial review.
        print('Private take received.' if receipt[0]['audio_sha256']==checksum else 'Earlier private take preserved.')
    else: raise SystemExit('Unknown operation.')


if __name__=='__main__':
    os.umask(0o077)
    run(sys.argv[1])
