# tf2-log-parser

A TF2 server log parser built for **[reconnexion.tf](https://reconnexion.tf)**, designed to move away from logs.tf dependency and give full control over match statistics.

## Requirements

- **Python 3**
- **[TFTrue](https://github.com/andrewbo29/tftrue)** — required for the additional log events this parser relies on

## Usage

```bash
python main.py <server_log>
```

## Output

The parser outputs a JSON object to stdout, with each player keyed by their Steam ID:

```json
{
  "U:1:962268762": {
    "name": "Jean-Paul Sartre",
    "kills": 0,
    "deaths": 0,
    "damage": 0,
    "classesPlayed": [],
    "team": ""
  }
}
```

Every player present in the log is included, regardless of when they joined or left.

## Notes

### Robustness
The parser is built to handle edge cases gracefully — if tournament mode behaves unexpectedly or players find ways to bug it, their stats won't be corrupted and the parser won't crash.

### Spy damage
Spy damage is currently inflated compared to other classes. A backstab deals 6× the target's health (double from the backstab bonus, triple from the crit multiplier), which significantly skews damage numbers. TFTrue does emit a `real_damage` event, but it fires *before* the backstab is registered, making it unreliable to use as a correction condition. This is a known limitation for now.
