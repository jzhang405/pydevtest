import click
import os
from typing import Tuple
from datetime import datetime
from pathlib import Path

# Enable Windows color support
try:
    import colorama
    colorama.init()
except ImportError:
    pass

class Config:
    def __init__(self):
        self.verbose = False

pass_config = click.make_pass_decorator(Config, ensure=True)

@click.group()
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode')
@click.version_option('0.1.0', prog_name='CLI Tool')
@click.pass_context
def main(ctx: click.Context, verbose: bool):
    """A sophisticated command line interface demo"""
    ctx.obj = Config()
    ctx.obj.verbose = verbose
    if verbose:
        click.echo("Verbose mode enabled")

@main.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--size', '-s', is_flag=True, help='Show file size')
@click.option('--modified', '-m', is_flag=True, help='Show last modified time')
@pass_config
def fileinfo(config: Config, path: str, size: bool, modified: bool):
    """Display file information"""
    if config.verbose:
        click.echo(f"Processing file: {path}")
    
    file_path = Path(path)
    info = []
    
    if size:
        file_size = file_path.stat().st_size
        info.append(f"Size: {click.style(str(file_size), fg='cyan')} bytes")
    
    if modified:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        info.append(f"Modified: {click.style(mtime.isoformat(), fg='yellow')}")
    
    if not info:
        info.append("No options selected. Use --size or --modified")
    
    click.echo('\n'.join(info))

@main.command()
@click.option('--upper', is_flag=True, help='Convert to uppercase')
@click.option('--repeat', '-r', default=1, type=click.IntRange(1, 10), 
             help='Repeat output (1-10 times)')
@click.argument('text', required=True)
@pass_config
def echo(config: Config, text: str, upper: bool, repeat: int):
    """Echo text with transformations"""
    if upper:
        text = text.upper()
    
    for _ in range(repeat):
        click.echo(click.style(text, fg='green', bold=True))
        if config.verbose:
            click.echo("---")

@main.command()
@click.option('--threshold', '-t', type=float, default=0.5,
             help='Threshold value (0.0-1.0)')
@click.argument('numbers', nargs=-1, type=float)
@pass_config
def analyze(config: Config, threshold: float, numbers: Tuple[float]):
    """Analyze numbers against threshold"""
    if not numbers:
        raise click.BadParameter("At least one number required")
    
    above = [n for n in numbers if n > threshold]
    below = [n for n in numbers if n <= threshold]
    
    click.echo(f"Numbers above {threshold}: {click.style(str(len(above)), fg='red')}")
    click.echo(f"Numbers below {threshold}: {click.style(str(len(below)), fg='blue')}")
    
    if config.verbose:
        click.echo(f"Total numbers processed: {len(numbers)}")

@main.command()
@click.password_option()
@click.option('--hash-type', type=click.Choice(['md5', 'sha1', 'sha256']), 
             default='sha256', show_default=True)
def encrypt(password: str, hash_type: str):
    """Encrypt a password"""
    import hashlib
    hash_obj = hashlib.new(hash_type)
    hash_obj.update(password.encode())
    click.echo(f"{hash_type}: {hash_obj.hexdigest()}")

if __name__ == '__main__':
    main()
