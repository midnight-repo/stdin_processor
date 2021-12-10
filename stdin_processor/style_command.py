import typer
from typing import List
from stdin_processor.processor import STDIN
from stdin_processor import global_args
import sys



def _style(x, **kwargs):
    foreground = kwargs.get('foreground', 'default')
    background = kwargs.get('background', 'default')
    bold = kwargs.get('bold', False)
    underline = kwargs.get('underline', False)
    blink = kwargs.get('blink', False)
    colors = {
        'red': typer.colors.RED,
        'bright_red': typer.colors.BRIGHT_RED,
        'green': typer.colors.GREEN,
        'bright_green': typer.colors.BRIGHT_GREEN,
        'cyan': typer.colors.CYAN,
        'bright_cyan': typer.colors.BRIGHT_CYAN,
        'blue': typer.colors.BLUE,
        'bright_blue': typer.colors.BRIGHT_BLUE,
        'yellow': typer.colors.YELLOW,
        'bright_yellow': typer.colors.BRIGHT_YELLOW,
        'magenta': typer.colors.MAGENTA,
        'bright_magenta': typer.colors.BRIGHT_MAGENTA,
        'black': typer.colors.BLACK,
        'bright_black': typer.colors.BRIGHT_BLACK,
        'white': typer.colors.WHITE,
        'bright_white': typer.colors.BRIGHT_WHITE,
        'default': typer.colors.RESET
    }

    return typer.style(x, fg=colors[foreground], bg=colors[background], bold=bold, underline=underline, blink=blink)





def style(foreground: str = typer.Option('default', '--color', '--fg'),
          background: str = typer.Option('default', '--background', '--bg'),
          bold: bool = typer.Option(False, '--bold', '-b'),
          underline: bool = typer.Option(False, '--underline', '--ul'),
          blink: bool = typer.Option(False, '--blink'),

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
    stdin.process(lambda x: _style(x, background=background, foreground=foreground, bold=bold, underline=underline, blink=blink),
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
                  start_where=start_where,
                  stop_where=stop_where,
                  _not=_not,
                  ignore_case=ignore_case,
                  indexes=indexes,
                  rotation=rotation,
                  reverse=reverse,
                  joiner=join)

    print(stdin.value, end='' if stdin.value.endswith('\n') else '\n')
