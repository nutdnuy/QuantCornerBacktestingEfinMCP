"""Copy only public skill resources to a host skill directory; never edit MCP config."""
import argparse, shutil
from pathlib import Path

def install(destination):
    source = Path(__file__).resolve().parents[1]
    target = Path(destination).expanduser() / 'quantcorner-backtesting-efin-mcp'
    if target.exists() or target.is_symlink():
        raise ValueError('Destination exists; review/remove or choose another destination. No overwrite.')
    target.parent.mkdir(parents=True, exist_ok=True)
    target.mkdir()
    # Explicit public resources; arbitrary files in the repository are not copied.
    files = ['SKILL.md', 'README.md', 'LICENSE', 'ASSETS_LICENSE.md', 'TESTING.md',
             'examples/report.html', 'examples/report-preview.png']
    groups = {'scripts': {'.py'}, 'tests': {'.py'}, 'agents': {'.yaml'},
              'references': {'.md'}, 'assets': {'.svg', '.woff2', '.txt'}}
    for name in files:
        path = source / name
        if path.is_file() and not path.is_symlink():
            dest = target / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)
    for folder, suffixes in groups.items():
        for path in (source / folder).rglob('*'):
            if (path.is_file() and not path.is_symlink() and path.suffix in suffixes
                    and '__pycache__' not in path.parts
                    and path.resolve().is_relative_to(source.resolve())):
                dest = target / path.relative_to(source)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, dest)
    return target

if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--target', choices=['codex','claude']);g.add_argument('--destination')
    a=p.parse_args()
    try:
        dest=Path.home()/('.codex' if a.target=='codex' else '.claude')/'skills' if a.target else Path(a.destination)
        print(install(dest))
    except (OSError,ValueError) as e:p.exit(2,str(e)+'\n')
