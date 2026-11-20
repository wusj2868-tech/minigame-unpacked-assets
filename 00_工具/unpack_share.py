"""Safely extract this archive; supports Windows long paths (stdlib only)."""
from pathlib import Path,PurePosixPath
import os,sys,zipfile,shutil
def main():
    if len(sys.argv)!=3:raise SystemExit('Usage: python unpack_share.py archive.zip output_directory')
    src=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
    if os.name=='nt':out=Path('\\\\?\\'+str(out))
    out.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(src) as z:
        infos=z.infolist()
        for k,i in enumerate(infos,1):
            p=PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in i.filename:raise ValueError('unsafe archive path')
            dest=out.joinpath(*p.parts)
            if i.is_dir():dest.mkdir(parents=True,exist_ok=True);continue
            dest.parent.mkdir(parents=True,exist_ok=True)
            with z.open(i) as r,dest.open('wb') as w:shutil.copyfileobj(r,w,1024*1024)
            if k%5000==0:print(f'{k}/{len(infos)} extracted',flush=True)
    print('Complete:',out)
if __name__=='__main__':main()
