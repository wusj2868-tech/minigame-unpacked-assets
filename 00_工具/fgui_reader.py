import struct
class R:
 def __init__(self,b,ss=None):self.b=b;self.p=0;self.ss=ss or []
 def val(self,f):v=struct.unpack_from('>'+f,self.b,self.p)[0];self.p+=struct.calcsize(f);return v
 def st(self):
  n=self.val('H');v=self.b[self.p:self.p+n].decode('utf8');self.p+=n;return v
 def s(self):
  n=self.val('H');return None if n==65534 else '' if n==65533 else self.ss[n]
 def seek(self,base,block):
  count=self.b[base];short=self.b[base+1]
  if block>=count:return False
  v=struct.unpack_from('>H' if short else '>I',self.b,base+2+block*(2 if short else 4))[0]
  if not v:return False
  self.p=base+v;return True
 def buf(self):
  n=self.val('I');r=R(self.b[self.p:self.p+n],self.ss);self.p+=n;return r

def parse(b):
 r=R(b);assert r.val('I')==0x46475549;ver=r.val('i');comp=r.val('B');pkgid=r.st();name=r.st();r.p+=20;idx=r.p;assert not comp
 r.seek(idx,4);r.ss=[r.st() for _ in range(r.val('i'))]
 if r.seek(idx,5):
  for _ in range(r.val('i')):
   i=r.val('H');n=r.val('i');r.ss[i]=r.b[r.p:r.p+n].decode();r.p+=n
 r.seek(idx,1);n=r.val('h');items=[]
 for _ in range(n):
  end=r.val('i')+r.p;ty=r.val('B');id=r.s();nm=r.s();path=r.s();file=r.s();exp=r.val('B');w=r.val('i');h=r.val('i');v={'type':ty,'id':id,'name':nm,'file':file,'width':w,'height':h}
  if ty==1:
   r.val('B');m=r.buf();m.seek(0,0);v['interval_ms']=m.val('i');v['swing']=m.val('B');v['repeat_delay_ms']=m.val('i');m.seek(0,1);nf=m.val('h');v['frame_count']=nf;frames=[]
   for _ in range(nf):
    e=m.val('H')+m.p;fr={'rect':[m.val('i') for _ in range(4)],'add_delay_ms':m.val('i'),'sprite_id':m.s()};frames.append(fr);m.p=e
   v['frames']=frames
  items.append(v);assert r.p<=end;r.p=end
 sprites=[]
 if r.seek(idx,2):
  for _ in range(r.val('h')):
   end=r.val('H')+r.p;sid=r.s();aid=r.s();rect=[r.val('i') for _ in range(4)];rot=r.val('B');sprites.append({'id':sid,'atlas_id':aid,'rect':rect,'rotated':rot});r.p=end
 return {'name':name,'id':pkgid,'version':ver,'items':items,'sprites':sprites}

