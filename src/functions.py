import os
import hashlib

def str_stat_inode(cur_stat):
    if cur_stat.st_ino == 0:
        raise Exception('Inode number zero')
    else:
        return str(cur_stat.st_ino)

def str_fname_inode(filename):
    cur_stat = os.stat(os.path.abspath(filename))
    try: 
        return str_stat_inode(cur_stat)
    except Exception:
        msum = hashlib.md5(filename)
        return msum.hexdigest()


