"""Export Cocos/FairyGUI PNG sprites, animation frames, GIF previews and JSON.
Input: original APK/ZIP or the root of its extracted file tree.
"""
from pathlib import Path
import argparse,collections,io,json,re,zipfile
from PIL import Image
from fgui_reader import parse

def safe(s):return re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',str(s)).rstrip('. ')[:150] or 'unnamed'
def uuid22(u):
    if len(u)!=22:return u
    alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    s=u[:2]
    for i in range(2,22,2):s+=format(alphabet.index(u[i])*64+alphabet.index(u[i+1]),'03x')
    return '-'.join([s[:8],s[8:12],s[12:16],s[16:20],s[20:]])

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);ap.add_argument('--no-gif',action='store_true');args=ap.parse_args()
    source=Path(args.input).resolve();out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=True)
    z=zipfile.ZipFile(source) if source.is_file() else None
    names=z.namelist() if z else [str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()]
    read=(lambda n:z.read(n)) if z else (lambda n:(source/n).read_bytes())
    packages=[];spriteframes=[];configs=[];failures=[];counts=collections.Counter()
    for n in names:
        if n.startswith('assets/res/raw-assets/') and n.endswith('.bin'):
            b=read(n)
            if b.startswith(b'FGUI'):
                p=parse(b);p['source']=n;packages.append(p)
        if n.startswith('assets/res/import/') and n.endswith('.json'):
            try:j=json.loads(read(n))
            except Exception:continue
            if isinstance(j,dict) and j.get('__type__')=='cc.SpriteFrame':spriteframes.append({'source':n,**j['content']})
            if isinstance(j,dict) and j.get('__type__')=='cc.JsonAsset':configs.append((n,j))
    index=out/'结构化索引';index.mkdir(exist_ok=True)
    (index/'FGUI全部包.json').write_text(json.dumps({'packages':packages,'cocos_spriteframes':spriteframes},ensure_ascii=False,indent=2))
    for p in packages:(index/(safe(p['name'])+'.json')).write_text(json.dumps(p,ensure_ascii=False,indent=2))
    conf=out/'配置JSON';conf.mkdir(exist_ok=True)
    for n,j in configs:
        (conf/(safe(j.get('_name') or Path(n).stem)+'.json')).write_text(json.dumps(j.get('json'),ensure_ascii=False,indent=2));counts['配置JSON']+=1
    sfbyname={s['name']:s for s in spriteframes};namesbytex=collections.defaultdict(list)
    for s in spriteframes:namesbytex[uuid22(s['texture'])].append(s['name'])
    images=out/'图集与独立图像';images.mkdir(exist_ok=True);native={}
    for n in names:
        if not n.startswith('assets/res/raw-assets/') or Path(n).suffix not in ['.png','.jpg']:continue
        u=Path(n).stem;native[u]=n;nm=sorted(namesbytex.get(u,[]));label=safe(nm[0] if nm else u)
        (images/(label+'__'+u[:8]+Path(n).suffix)).write_bytes(read(n));counts['原始图像']+=1
    cache={}
    def atlas(package,atlas_id):
        it=next(x for x in package['items'] if x['id']==atlas_id);key=package['name']+'_'+Path(it.get('file') or atlas_id).stem
        if key not in cache:
            u=uuid22(sfbyname[key]['texture']);cache[key]=Image.open(io.BytesIO(read(native[u]))).convert('RGBA')
        return cache[key]
    def sprite(package,s):
        im=atlas(package,s['atlas_id']);x,y,w,h=s['rect'];p=im.crop((x,y,x+(h if s['rotated'] else w),y+(w if s['rotated'] else h)))
        return p.transpose(Image.Transpose.ROTATE_90) if s['rotated'] else p
    for number,p in enumerate(packages,1):
        sp={s['id']:s for s in p['sprites']}
        for it in p['items']:
            if it['type'] not in [0,1]:continue
            label=safe(it.get('name') or it['id'])+'__'+safe(it['id'])
            try:
                if it['type']==0:
                    if it['id'] not in sp:continue
                    d=out/'独立精灵PNG'/safe(p['name']);d.mkdir(parents=True,exist_ok=True);sprite(p,sp[it['id']]).save(d/(label+'.png'),compress_level=2);counts['精灵PNG']+=1
                else:
                    d=out/'动画PNG帧'/safe(p['name'])/label;d.mkdir(parents=True,exist_ok=True);frames=[];times=[]
                    for k,fr in enumerate(it['frames']):
                        image=Image.new('RGBA',(it['width'],it['height']))
                        if fr.get('sprite_id') in sp:image.alpha_composite(sprite(p,sp[fr['sprite_id']]),(fr['rect'][0],fr['rect'][1]))
                        image.save(d/f'{k:03d}.png',compress_level=2);counts['动画帧PNG']+=1;frames.append(image);times.append(it['interval_ms']+fr['add_delay_ms'])
                    (d/'动画配置.json').write_text(json.dumps(it,ensure_ascii=False,indent=2));counts['动画定义']+=1
                    if frames and not args.no_gif:
                        g=out/'GIF预览'/safe(p['name']);g.mkdir(parents=True,exist_ok=True)
                        frames[0].save(g/(label+'.gif'),save_all=True,append_images=frames[1:],duration=times,loop=0,disposal=2);counts['GIF预览']+=1
            except Exception as ex:failures.append({'package':p['name'],'item':it.get('name'),'id':it['id'],'error':str(ex)[:300]})
        if number%10==0:print(json.dumps({'packages_done':number,'total':len(packages),'exports':dict(counts)},ensure_ascii=False),flush=True)
    summary={'counts':dict(counts),'packages':len(packages),'failures':failures,'note':'PNG sprites are atlas regions; GIF timing follows MovieClip configuration including per-frame delay. UI components, shaders and gameplay timing are not reconstructed.'}
    (out/'_导出总表.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print('COMPLETE '+json.dumps(summary,ensure_ascii=False),flush=True)

if __name__=='__main__':main()
