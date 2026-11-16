"""Publish the S017 caption-timing correction as a new, non-overwriting asset."""
from datetime import datetime,timezone
from hashlib import sha256
import base64
import json
from pathlib import Path
import subprocess
import time

from publish import BRANCH,CATALOGUE,REPOSITORY,api,check_upload,get_catalogue,gh
from render import HERE

EXPECTED_LIVE='8c88053cb5a765f0d705b2a6e84b76af195f66bf71feb32675d5b8e'


def main(out):
    timeline=json.loads((HERE/'S017.json').read_text())
    report=json.loads((out/'S017-qa.json').read_text())
    _,catalogue=get_catalogue()
    row=next(x for x in catalogue['entries'] if x['id']=='S017')
    if row.get('illustration')==1 and row.get('illustratedRevision')==2:
        assert row['sha256']==report['sha256']
        print('S017 v2 is already selected')
        return
    assert row['illustration']==1 and row['sha256']==EXPECTED_LIVE
    assert row['legacy_sha256']==timeline['legacy_sha256'] and row['seconds']==report['seconds']
    assets=json.loads(gh('release','view','lesson-introductions','--repo',REPOSITORY,'--json','assets'))['assets']
    present={asset['name'] for asset in assets}
    for suffix in ('.mp4','-poster.jpg'):
        original=out/('S017-Intro-Illustrated'+suffix)
        revised=out/('S017-Intro-Illustrated-v2'+suffix)
        revised.write_bytes(original.read_bytes())
        digest=sha256(revised.read_bytes()).hexdigest()
        if suffix=='.mp4':assert digest==report['sha256']
        if revised.name not in present:
            gh('release','upload','lesson-introductions',str(revised),'--repo',REPOSITORY)
        check_upload(revised.name,digest)
    for attempt in range(8):
        previous,catalogue=get_catalogue()
        row=next(x for x in catalogue['entries'] if x['id']=='S017')
        if row.get('illustration')==1 and row.get('illustratedRevision')==2:
            assert row['sha256']==report['sha256']
            return
        assert row['illustration']==1 and row['sha256']==EXPECTED_LIVE
        row.update(illustration=1,illustratedRevision=2,previous_illustrated_sha256=EXPECTED_LIVE,sha256=report['sha256'],
                   illustrated_at=datetime.now(timezone.utc).isoformat())
        content=json.dumps(catalogue,ensure_ascii=False,separators=(',',':'))+'\n'
        try:
            api(f'contents/{CATALOGUE}',{'branch':BRANCH,'sha':previous,
                'message':'Correct lesson 17 caption timing',
                'content':base64.b64encode(content.encode()).decode()})
        except subprocess.CalledProcessError:
            if attempt==7:raise
            time.sleep(3)
        else:
            print('S017 v2: new release bytes and seeking verified; original asset preserved')
            return


if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True)
    main(parser.parse_args().out)
