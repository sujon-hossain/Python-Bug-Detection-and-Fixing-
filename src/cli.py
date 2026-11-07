"""Interactive command line interface."""
from . import bases, stats
from .calculator import Calculator, format_number
from .converter import convert
from .errors import CalcError
from .functions import require_int

HELP = """Type an expression (2+3*4, sqrt(16), x = 5, ans*2) or a command:
  history [n]           show the last n calculations
  clear                 clear the history
  mode [deg|rad]        show or set the angle mode
  convert V FROM TO     e.g. convert 5 km mi
  stats N1 N2 ...       count, mean, median, mode, stdev
  bin|oct|hex EXPR      show a whole number in base 2, 8 or 16
  frombase DIGITS BASE  e.g. frombase ff 16
  ms|m+|m- [EXPR]       store in / add to / subtract from memory
  mr | mc               recall / clear memory
  help | quit"""


def _parse_number(token):
    try:
        return float(token)
    except ValueError:
        raise CalcError(f"Invalid number '{token}'")


def _with_prefix(digits, prefix):
    return prefix + digits


def cmd_help(calc, rest):
    return HELP


def cmd_quit(calc, rest):
    return None


def cmd_history(calc, rest):
    try:
        n = int(rest) if rest else 10
    except ValueError:
        raise CalcError("history takes a whole number")
    entries = calc.history.recent(n)
    if not entries:
        return "History is empty."
    return "\n".join(
        f"{i}. {e.expression} = {format_number(e.result)}"
        for i, e in enumerate(entries)
    )


def cmd_clear(calc, rest):
    calc.history.clear()
    return "History cleared."


def cmd_mode(calc, rest):
    if rest:
        calc.env.set_angle_mode(rest.lower())
    return f"Angle mode: {calc.env.angle_mode}"


def cmd_convert(calc, rest):
    parts = rest.split()
    if len(parts) != 3:
        raise CalcError("Usage: convert VALUE FROM TO")
    value = _parse_number(parts[0])
    result = convert(value, parts[2], parts[1])
    return f"{format_number(value)} {parts[1]} = {format_number(result)} {parts[2]}"


def cmd_stats(calc, rest):
    values = [_parse_number(t) for t in rest.split()]
    modes = stats.mode(values)
    mode_text = ", ".join(format_number(m) for m in modes) if modes else "none"
    return "\n".join([
        f"count: {len(values)}",
        f"mean: {format_number(stats.mean(values))}",
        f"median: {format_number(stats.median(values))}",
        f"mode: {mode_text}",
        f"stdev: {format_number(stats.stdev(values))}",
    ])


def _make_base_command(base, prefix):
    def command(calc, rest):
        n = require_int("base conversion", calc.evaluate(rest))
        return _with_prefix(bases.to_base(n, base), prefix)
    return command


def cmd_frombase(calc, rest):
    parts = rest.split()
    if len(parts) != 2:
        raise CalcError("Usage: frombase DIGITS BASE")
    try:
        base = int(parts[1])
    except ValueError:
        raise CalcError("BASE must be a whole number")
    return str(bases.from_base(parts[0], base))


def _memory_operand(calc, rest):
    if rest:
        return calc.evaluate(rest)
    ans = calc.env.variables.get("ans")
    if ans is None:
        raise CalcError("Give an expression or calculate something first")
    return ans


def _memory_report(calc):
    return f"M = {format_number(calc.memory.recall())}"


def cmd_ms(calc, rest):
    calc.memory.store(_memory_operand(calc, rest))
    return _memory_report(calc)


def cmd_mplus(calc, rest):
    calc.memory.add(_memory_operand(calc, rest))
    return _memory_report(calc)


def cmd_mminus(calc, rest):
    calc.memory.subtract(_memory_operand(calc, rest))
    return _memory_report(calc)


def cmd_mr(calc, rest):
    return _memory_report(calc)


def cmd_mc(calc, rest):
    calc.memory.clear()
    return _memory_report(calc)


COMMANDS = {
    "help": cmd_help, "quit": cmd_quit, "exit": cmd_quit,
    "history": cmd_history, "clear": cmd_clear, "mode": cmd_mode,
    "convert": cmd_convert, "stats": cmd_stats,
    "bin": _make_base_command(2, "0b"),
    "oct": _make_base_command(8, "0o"),
    "hex": _make_base_command(16, "0x"),
    "frombase": cmd_frombase,
    "ms": cmd_ms, "m+": cmd_mplus, "m-": cmd_mminus, "mr": cmd_mr, "mc": cmd_mc,
}


def process_line(calc, line):
    """Return the text to print, '' for blank input, or None to quit."""
    line = line.strip()
    if not line:
        return ""
    cmd, _, rest = line.partition(" ")
    cmd = cmd.lower()
    rest = rest.strip()
    try:
        if "=" not in line and cmd in COMMANDS:
            return COMMANDS[cmd](calc, rest)
        return format_number(calc.evaluate(line))
    except CalcError as exc:
        return f"Error: {exc}"


def main():
    calc = Calculator()
    print("Debug-Practice Calculator. Type 'help' for commands, 'quit' to exit.")
    while True:
        try:
            line = input("calc> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        output = process_line(calc, line)
        if output is None:
            break
        if output:
            print(output)
