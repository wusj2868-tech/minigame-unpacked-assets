"""Verify every listed file in this ZIP or in its extracted root (stdlib only)."""
from pathlib import Path
import argparse,csv,hashlib,io,zipfile
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');args=p.parse_args();src=Path(args.input)
    z=zipfile.ZipFile(src) if src.is_file() else None
    read=(lambda n:z.open(n)) if z else (lambda n:(src/n).open('rb'))
    with read('00_文件校验清单.csv') as f:rows=list(csv.DictReader(io.StringIO(f.read().decode('utf-8-sig'))))
    failed=[]
    for k,row in enumerate(rows,1):
        h=hashlib.sha256();size=0
        try:
            with read(row['path']) as f:
                while True:
                    b=f.read(1024*1024)
                    if not b:break
                    h.update(b);size+=len(b)
            if size!=int(row['bytes']) or h.hexdigest()!=row['sha256']:failed.append(row['path'])
        except Exception as e:failed.append(row['path']+': '+str(e))
        if k%5000==0:print(f'{k}/{len(rows)} checked',flush=True)
    print('Files checked:',len(rows),'Failures:',len(failed))
    for n in failed[:30]:print(n)
    raise SystemExit(1 if failed else 0)
if __name__=='__main__':main()
