import csv,math,os,argparse
import numpy as np
from PIL import Image

def read_col(path):
    with open(path,'r',encoding='utf-8-sig') as f:
        r=csv.reader(f);next(r,None)
        return [int(float(x[0])) for x in r if x and x[0].strip().isdigit() and int(float(x[0]))>0]

def spiral(L):
    g=np.zeros((L,L),int);r=c=L//2;n=1;g[r,c]=1
    def mv(dr,dc,s,r,c,n):
        for _ in range(s):
            if n>=L*L:return r,c,n
            r+=dr;c+=dc;n+=1;g[r,c]=n
        return r,c,n
    s=1
    while n<L*L:
        for d in [(0,1),(-1,0),(0,-1),(1,0)]:
            r,c,n=mv(*d,s,r,c,n)
            if d==( -1,0) or d==(1,0):s+=1
            if n>=L*L:break
    return g

def draw(ids,out='99.png',cell=1):
    m=max(ids);L=math.ceil(math.sqrt(m));L+=L%2==0
    g=spiral(L);mask=np.isin(g,ids)
    img=np.where(mask,0,255).astype('uint8')
    if cell>1:img=np.repeat(np.repeat(img,cell,0),cell,1)
    Image.fromarray(img).save(out)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument('--csv',default='sorted1.csv')
    p.add_argument('--out',default='99.png')
    p.add_argument('--cell',type=int,default=1)
    a=p.parse_args()
    if not os.path.exists(a.csv):raise FileNotFoundError(a.csv)
    ids=read_col(a.csv)
    draw(ids,a.out,a.cell)
    print("saved",a.out)
