"""Export readable assets from standard Unity bundles and the verified 0xef35 variant.

Input may be an APK/ZIP or an extracted directory. This does NOT decrypt Blue Planet's
protected bundles. Failed objects retain their original source in the sharing archive.
"""
from pathlib import Path
import argparse,collections,concurrent.futures,contextlib,hashlib,io,json,re,struct,time,zipfile
import UnityPy,lz4.block

_ZIPS={}
def safe(s):
    s=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',str(s)).rstrip('. ') or 'unnamed'
    return s if len(s)<=135 else s[:120]+'_'+hashlib.sha1(s.encode()).hexdigest()[:10]

def custom_environment(b):
    if not b.startswith(b'UnityFS\0'):raise ValueError('not UnityFS')
    off=b.index(0)+5
    for _ in range(2):off=b.index(0,off)+1
    size,cs,us,flags=struct.unpack_from('>QIII',b,off);off=(off+20+15)//16*16
    if size!=len(b):raise ValueError('bundle size mismatch')
    inf=lz4.block.decompress(b[off:off+cs],uncompressed_size=us)
    count=struct.unpack_from('>I',inf,16)[0];pos=(off+cs+15)//16*16;parts=[];custom=False
    for k in range(count):
        u,c,fl=struct.unpack_from('>IIH',inf,20+k*10);raw=b[pos:pos+c]
        if fl==0xef35:custom=True;dec=lz4.block.decompress(raw,uncompressed_size=u)
        elif fl&63 in [2,3]:dec=lz4.block.decompress(raw,uncompressed_size=u)
        elif fl&63==0:dec=raw
        else:raise ValueError('unsupported/protected block '+hex(fl))
        if len(dec)!=u:raise ValueError('block size mismatch')
        parts.append(dec);pos+=c
    if not custom:raise ValueError('not the verified 0xef35 variant')
    if pos!=len(b):raise ValueError('block extent mismatch')
    data=b''.join(parts);i=20+count*10;n=struct.unpack_from('>I',inf,i)[0];i+=4
    env=UnityPy.Environment()
    for _ in range(n):
        start,length,fl=struct.unpack_from('>QQI',inf,i);i+=20;end=inf.index(0,i);name=inf[i:end].decode();i=end+1
        if start+length>len(data):raise ValueError('node extent mismatch')
        env.load_file(data[start:start+length],name=name)
    return env

def json_default(v):
    if isinstance(v,(bytes,bytearray)):return {'__bytes_hex__':bytes(v).hex()}
    if hasattr(v,'tolist'):return v.tolist()
    raise TypeError(type(v).__name__)

def write_json(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=json_default),encoding='utf-8')

def export_one(job):
    source,entry,outroot,iszip=job
    result={'source':entry,'exports':collections.Counter(),'failures':[],'skipped':[],'custom_0xef35':False}
    try:
        if iszip:
            if source not in _ZIPS:_ZIPS[source]=zipfile.ZipFile(source)
            b=_ZIPS[source].read(entry)
        else:b=(Path(source)/entry).read_bytes()
        try:
            with contextlib.redirect_stdout(io.StringIO()):env=UnityPy.load(b)
        except Exception:
            env=custom_environment(b);result['custom_0xef35']=True
        objs=list(env.objects)
        if not objs:raise ValueError('no serialized objects')
        folder=Path(outroot)/safe(Path(entry).name);folder.mkdir(parents=True,exist_ok=True)
        types=collections.Counter(o.type.name for o in objs);meta={'source':entry,'object_counts':dict(types),'textures':[],'animation_names':[],'custom_0xef35':result['custom_0xef35']}
        used=set()
        for o in objs:
            typ=o.type.name
            if typ not in ['Texture2D','TextAsset','Mesh','AnimationClip','Material','Font']:continue
            try:
                d=o.read();name=safe(getattr(d,'m_Name','') or f'{typ}_{o.path_id}')
                if typ=='Texture2D':
                    if d.m_Width<=0 or d.m_Height<=0:
                        result['skipped'].append({'type':typ,'path_id':o.path_id,'name':name,'reason':'zero-sized runtime-generated texture; no static bitmap'});continue
                    if d.m_TextureFormat==20:
                        raw=d.get_image_data();fn=name+f'__{o.path_id}.rgba32f';(folder/fn).write_bytes(raw)
                        write_json(folder/(fn+'.json'),{'width':d.m_Width,'height':d.m_Height,'unity_texture_format':20,'format':'RGBAFloat, 4 float32 channels per pixel','byte_length':len(raw),'mips':d.m_MipCount,'note':'Data texture preserved as raw float values, not converted into lossy 8-bit PNG.'});result['exports']['FloatTexture_DATA']+=1;continue
                    filename=name+'.png'
                    if filename in used:filename=name+f'__{o.path_id}.png'
                    d.image.save(folder/filename,compress_level=2);used.add(filename);result['exports']['PNG']+=1
                    meta['textures'].append({'file':filename,'width':d.m_Width,'height':d.m_Height,'format':d.m_TextureFormat})
                elif typ=='TextAsset':
                    raw=d.m_Script
                    if isinstance(raw,str):raw=raw.encode('utf-8','surrogateescape')
                    filename=name if Path(name).suffix else name+'.bytes'
                    if filename in used:filename=name+f'__{o.path_id}.bytes'
                    (folder/filename).write_bytes(raw);used.add(filename);result['exports']['TextAsset']+=1
                elif typ=='Font':
                    raw=bytes(d.m_FontData)
                    if raw:
                        ext='.otf' if raw.startswith(b'OTTO') else '.ttf';(folder/(name+f'__{o.path_id}'+ext)).write_bytes(raw);result['exports']['FontFile']+=1
                elif typ=='Mesh':
                    (folder/(name+f'__{o.path_id}.obj')).write_text(d.export(),encoding='utf-8');result['exports']['OBJ']+=1
                elif typ in ['AnimationClip','Material']:
                    write_json(folder/(name+f'__{o.path_id}.{typ}.json'),o.read_typetree());result['exports'][typ+'_JSON']+=1
                    if typ=='AnimationClip':meta['animation_names'].append(name)
            except Exception as ex:result['failures'].append({'type':typ,'path_id':o.path_id,'error':str(ex)[:350]})
        write_json(folder/'_资源说明.json',meta)
        result['object_counts']=dict(types)
    except Exception as ex:result['bundle_error']=str(ex)[:450]
    result['exports']=dict(result['exports']);return result

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input',required=True,help='APK/ZIP or extracted directory')
    ap.add_argument('--output',required=True);ap.add_argument('--workers',type=int,default=3)
    ap.add_argument('--limit',type=int,default=0,help='Optional sample limit; 0 means all supported Unity file extensions')
    args=ap.parse_args();source=Path(args.input).resolve();output=Path(args.output).resolve();output.mkdir(parents=True,exist_ok=True)
    iszip=source.is_file()
    suffixes=('.ab','.unity3d','.bundle','.assets')
    if iszip:
        with zipfile.ZipFile(source) as z:entries=[n for n in z.namelist() if n.lower().endswith(suffixes)]
    else:entries=[str(p.relative_to(source)) for p in source.rglob('*') if p.is_file() and p.suffix.lower() in suffixes]
    if args.limit:entries=entries[:args.limit]
    jobs=[(str(source),n,str(output),iszip) for n in entries];records=[];counts=collections.Counter();started=time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.workers) as pool:
        for i,r in enumerate(pool.map(export_one,jobs,chunksize=8),1):
            records.append(r);counts.update(r['exports'])
            if i%100==0 or i==len(jobs):print(json.dumps({'done':i,'total':len(jobs),'exported':dict(counts),'seconds':round(time.time()-started)},ensure_ascii=False),flush=True)
    summary={'source_name':source.name,'bundles_attempted':len(records),'bundle_failures':sum('bundle_error' in r for r in records),'object_failures':sum(len(r['failures']) for r in records),'skipped_runtime_textures':sum(len(r.get('skipped',[])) for r in records),'exports':dict(counts),'records':records,'note':'PNG is the decoded texture page, not necessarily an assembled pose. OBJ does not preserve rigging or animation. Raw bundles remain the authoritative source.'}
    write_json(output/'_导出总表.json',summary)
    print('COMPLETE '+json.dumps({k:v for k,v in summary.items() if k!='records'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
