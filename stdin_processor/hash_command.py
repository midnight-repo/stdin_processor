import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
import hashlib

def _hash(string, **kwargs):
    alg = kwargs.get('alg')
    l = kwargs.get('list', False)

    algs = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha284': hashlib.sha3_384,
        'sha512': hashlib.sha3_512
    }

    if l:
        for a in algs:
            print(a)
        exit()

    return algs[alg](string.strip().encode()).hexdigest()




def hash(alg: str = typer.Argument(..., help='Encoding to use'),
           list: bool = typer.Option(False, help='List encodings'),

           ____________________________: str = global_args.args_separator,
           separators: List[str] = global_args.separators,
           group_by: int = global_args.group_by,
           group_join: str = global_args.group_join,
           join: str = global_args.join,
           unique: bool = global_args.unique,
           sort: str = global_args.sort,
           sort_key: str = global_args.sort_key,
           keep: bool = global_args.keep,
           where: List[str] = global_args.where,
           indexes: str = global_args.index,
           _not: bool = global_args._not,
           ignore_case: bool = global_args.ignore_case
           ):


    stdin = STDIN()
    stdin.process(lambda x: _hash(x, alg=alg, list=list),
                  separators=separators,
                  group_by=group_by,
                  group_join=group_join,
                  unique=unique,
                  sort=sort,
                  sort_key=sort_key,
                  keep=keep,
                  where=where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  joiner=join)

    print(stdin.value, end='\n' if '\n' in separators else '')
