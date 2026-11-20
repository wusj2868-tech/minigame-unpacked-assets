from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,shutil,subprocess,zipfile
ROOT=Path(__file__).resolve().parent
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser(description='Download one complete game ZIP from GitHub Releases.');p.add_argument('--game',default='all',choices=['all','01','02','03','04']);p.add_argument('--list',action='store_true');p.add_argument('--output',default='downloads');p.add_argument('--extract',action='store_true');p.add_argument('--remove-zip',action='store_true');a=p.parse_args()
 j=json.loads((ROOT/'catalog/projects.json').read_text(encoding='utf8'));selected=[g for g in j['projects'] if a.game=='all' or g['id']==a.game]
 if a.list:
  for g in selected:print(g['id'],g['name'],g['version'],g['status'],f"{g.get('zip_bytes',g['estimated_zip_bytes'])/1e6:.1f} MB",g['asset_name'])
  return
 if not shutil.which('gh'):raise SystemExit('GitHub CLI (gh) is required. You may instead download through the README links in a browser.')
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 for g in selected:
  if g['status']!='uploaded' or not g.get('sha256'):raise SystemExit('Project not yet ready: '+g['name'])
  f=out/g['asset_name']
  if f.exists() and sha(f)!=g['sha256']:raise SystemExit('Existing ZIP has a different checksum; move it aside first: '+str(f))
  if not f.exists():subprocess.run(['gh','release','download',j['release'],'--repo',j['repository'],'--pattern',g['asset_name'],'--dir',str(out)],check=True)
  if sha(f)!=g['sha256']:raise SystemExit('SHA256 mismatch: '+str(f))
  print('SHA256 OK:',g['name'],flush=True)
  if a.extract:
   dest=out/'unpacked'/g['slug']
   if dest.exists():raise SystemExit('Extraction target already exists; move it aside first: '+str(dest))
   actual=Path('\\\\?\\'+str(dest)) if os.name=='nt' else dest;actual.mkdir(parents=True)
   with zipfile.ZipFile(f) as z:
    for i in z.infolist():
     rel=PurePosixPath(i.filename)
     if rel.is_absolute() or '..' in rel.parts or '\\' in i.filename:raise ValueError('Unsafe archive path')
     target=actual.joinpath(*rel.parts)
     if i.is_dir():target.mkdir(parents=True,exist_ok=True);continue
     target.parent.mkdir(parents=True,exist_ok=True)
     with z.open(i) as r,target.open('wb') as w:shutil.copyfileobj(r,w,1024*1024)
   print('Extracted:',dest,flush=True)
   if a.remove_zip:f.unlink()
if __name__=='__main__':main()
