import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
import random
import string as chars

def hide(
        ______________: str = global_args.args_separator,
        separators: List[str] = global_args.separators,
        clean: bool = global_args.clean,
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
    # stdin.process(lambda x: x,
    #               separators=separators,
    #               clean=clean,
    #               group_by=group_by,
    #               group_join=group_join,
    #               unique=unique,
    #               sort=sort,
    #               sort_key=sort_key,
    #               keep=keep,  # True MAKES NO SENSE IN SHOW COMMAND
    #               where=where,
    #               _not=_not, # difference with show
    #               ignore_case=ignore_case,
    #               indexes=indexes,
    #               joiner=join)


    # THIS IS JUST A WORKAROUND, TEMPORARY FIX
    # if match, append random_val to list, before printing, remove random_val from list
    # if we append '' instead of random_val, it will interfere with --clean option
    random_val = '!_-<{[(==!-%s-!==)]}>-_!' % ''.join([random.choice(chars.ascii_letters + chars.digits) for i in range(64)])
    stdin.split(*separators, clean=clean)
    if group_by > 1:
        stdin.group_by(group_by, group_join)
    stdin.match(*where, ignore_case=ignore_case, index_pattern=indexes, keep=keep, _not=_not)
    stdin.map(lambda x: random_val)
    while random_val in stdin.value:
        stdin.value.remove(random_val)
    if unique:
        stdin.remove_duplicates()
    if sort != 'False':
        stdin.sort(sort, sort_key=sort_key)
    stdin.join(join)

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
