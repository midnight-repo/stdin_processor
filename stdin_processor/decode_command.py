import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
from urllib.parse import unquote, unquote_plus
import base64
import binascii



def _decode(string, **kwargs):
    encoding = kwargs.get('encoding')
    l = kwargs.get('list', False)

    encodings = {
        'url': unquote,
        'urlp': unquote_plus,
        'b64': base64.b64decode,
        'b32': base64.b32decode,
        'b16': binascii.unhexlify,
        'hex': binascii.unhexlify
    }

    if l == True:
        for e in encodings:
            print(e)
        exit()
    else:
        if encoding in ['b64', 'b32', 'b16', 'hex']:
            return encodings[encoding](string).decode()
        else:
            return encodings[encoding](string)




def decode(encoding: str = typer.Argument(..., help='Encoding to use'),
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
    stdin.process(lambda x: _decode(x, encoding=encoding, list=list),
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
