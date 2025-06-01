from . import start
from . import help
from . import echo

__all__ = ["start", "help", "echo"]
"""
all - содержит список модулей которые импортируются.
допустим если бы тут был лишний файл, который при импорте hendlers нам был бы не нужен
мы бы его просто НЕ вписали в этот список и тогда при записи
from handlers import * - мы бы импортировали только модули: 'start', 'help', 'echo'
"""
