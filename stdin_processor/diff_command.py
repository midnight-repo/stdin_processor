import sys
import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
import subprocess
import random
from collections import deque


def _diff(standard_input, command, both_ways):
    difference = []
    for element in standard_input:
        if not element in command:
            difference.append(element)

    if both_ways == True:
        for element in command:
            if not element in standard_input:
                difference.append(element)

    return difference


def diff(command: str = typer.Argument(..., help='the command to substract to standard input'),
         both_ways: bool = typer.Option(False, '--both-ways/--no-bothways', '-b/--nb',
                                        help='Shows the difference between stdin and command AND between command and stdin'),
         ____________________________: str = global_args.args_separator,
         separators: List[str] = global_args.separators,
         clean: bool = global_args.clean,
         group_by: int = global_args.group_by,
         group_join: str = global_args.group_join,
         join: str = global_args.join,
         unique: bool = global_args.unique,
         sort: str = global_args.sort,
         sort_key: str = global_args.sort_key,
         shuffle: bool = global_args.shuffle,
         keep: bool = global_args.keep,
         where: List[str] = global_args.where,
         start_where: str = global_args.start_where,
         stop_where: str = global_args.stop_where,
         indexes: str = global_args.index,
         _not: bool = global_args._not,
         rotation: int = global_args.rotation,
         reverse: bool = global_args.reverse,
         ignore_case: bool = global_args.ignore_case
         ):
    stdin = STDIN(sys.stdin.read())
    stdin.split(*separators, clean=clean)
    if group_by > 1:
        stdin.group_by(group_by, group_join)
    if rotation != 0:
        val = deque(stdin.value)
        val.rotate(rotation)
        stdin.value = val
    stdin.between(start_where, stop_where)
    if shuffle:
        random.shuffle(stdin.value)
    stdin.match(*where, ignore_case=ignore_case, index_pattern=indexes, keep=keep, _not=_not)
    stdin.map(lambda x: x)
    if unique:
        stdin.remove_duplicates()
    if reverse:
        stdin.reverse()
    if sort != 'False':
        stdin.sort(sort, sort_key=sort_key)



    command_output = STDIN(subprocess.getoutput(command))
    command_output.split(*separators, clean=clean)
    if group_by > 1:
        command_output.group_by(group_by, group_join)
    if rotation != 0:
        val = deque(command_output.value)
        val.rotate(rotation)
        command_output.value = val
    stdin.between(start_where, stop_where)
    if shuffle:
        random.shuffle(command_output.value)
    command_output.match(*where, ignore_case=ignore_case, index_pattern=indexes, keep=keep, _not=_not)
    command_output.map(lambda x: x)
    if unique:
        command_output.remove_duplicates()
    if reverse:
        stdin.reverse()
    if sort != 'False':
        command_output.sort(sort, sort_key=sort_key)

    diff_output = join.join(_diff(stdin.value, command_output.value, both_ways))
    print(diff_output, end='' if diff_output.endswith('\n') else '\n')
