import typer
import sys
import os



package_path = '/'.join(__file__.split('/')[:-1])



# This is for testing ===========================
d = '/'.join(os.getcwd().split('/')[:-1])
sys.path.append(d)

if package_path == '':
    package_path = os.getcwd()
# ===============================================


# import commands
imports = {}
for file in os.listdir(package_path):
    if file.endswith('_command.py'):
        i = file[:-3]
        f = file.split('_')[0]
        i = __import__(f'stdin_processor.{i}', fromlist=[f])
        imports[f] = getattr(i, f)


def run():
    app = typer.Typer()
    decorate = app.command()
    [decorate(func) for func in imports.values()]
    app()




if __name__ == '__main__':
    run()







