"""Fixed destructive controls use temporary copies, never author artifacts."""
import contextlib, io, json, shutil, tempfile
from pathlib import Path
import verify_engineering as v

def must_reject(label, mutation):
    old_r,old_raw=v.R,v.RAW
    try:
        with tempfile.TemporaryDirectory(prefix='eng004-review-') as name:
            root=Path(name);v.R=root/'results';v.R.mkdir();v.RAW=old_raw
            for file in old_r.glob('*.json'):shutil.copy2(file,v.R/file.name)
            mutation(root)
            try:
                with contextlib.redirect_stdout(io.StringIO()):v.main()
            except AssertionError:
                print(label+': REJECTED_AS_REQUIRED');return
            raise RuntimeError(label+' was accepted')
    finally:v.R,v.RAW=old_r,old_raw

def wrong_j(root):
    f=v.R/'sensitivities.json';x=json.loads(f.read_text());x[0]['saltation_jacobian'][0][0]+=.1;f.write_text(json.dumps(x))
def wrong_raw(root):
    v.RAW=root/'raw';v.RAW.mkdir();name='nominal-7-1.0.bin';(v.RAW/name).write_bytes((v.R/'..'/'unused').name.encode())
# Only first archive is needed: the integrity guard must reject it before iteration.
must_reject('changed published Jacobian',wrong_j)
must_reject('corrupted raw archive',wrong_raw)
