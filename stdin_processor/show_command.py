import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args


def show(
        ______________: str = global_args.args_separator,
        separators: List[str] = global_args.separators,
        clean: bool = global_args.clean,
        group_by: int = global_args.group_by,
        group_join: str = global_args.group_join,
        join: str = global_args.join,
        unique: bool = global_args.unique,
        sort: str = global_args.sort,
        sort_key: str = global_args.sort_key,
        shuffle: bool = global_args.shuffle,
        keep: bool = typer.Option(False, '--keep/--no-keep', '-k/--nk', help='Keep the elements that that did not match --where or --index'),
        where: List[str] = global_args.where,
        indexes: str = global_args.index,
        _not: bool = global_args._not,
        ignore_case: bool = global_args.ignore_case
):


    stdin = STDIN()
    stdin.process(lambda x: x,
                  separators=separators,
                  clean=clean,
                  group_by=group_by,
                  group_join=group_join,
                  unique=unique,
                  sort=sort,
                  sort_key=sort_key,
                  shuffle=shuffle,
                  keep=keep,
                  where=where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  joiner=join)

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
