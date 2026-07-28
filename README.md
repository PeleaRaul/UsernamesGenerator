# MC Username Generator v2

A companion app to **CyberScan Suite** and **ProxyScraper v3**.
Generates random, syntactically valid Minecraft Java Edition usernames using a built-in database of 600+ real first names.

## What's New in v2

- **Realistic mode** — generates usernames from real first names like `Andrew123`, `sarah456`, `Mike_99`
- **628 built-in first names** covering all 26 letters A-Z
- **Case variations** — names appear as `Andrew123`, `andrew123`, or `Andrew123` randomly
- **Smart suffix generation** — appends 1-4 digit numbers, optional underscore separators
- **Original random mode** still available as a toggle

## Features

- **Generation mode toggle** — Realistic (real names + numbers) or Random (pure alphanumeric)
- **Starting letter selector** (A-Z dropdown + "Random" button)
- **Length range sliders** — min and max between 3 and 16 characters (Minecraft's limit)
- **Character options** — toggle numbers (0-9) and underscores (_)
- **Unique mode** — case-insensitive duplicate elimination
- **Quantity slider** — 1 to 10,000, with custom entry supporting up to 50,000
- **Pool estimation** — warns if you request more unique names than possible
- **Export** — copy to clipboard or save to timestamped `.txt` file
- **Background threading** — stays responsive even at 10,000+ names
- **Dark green cyber theme** — matches CyberScan Suite & ProxyScraper v3

## Minecraft Java Username Rules (enforced)

| Rule | Constraint |
|------|-----------|
| Length | 3-16 characters |
| First character | Must be a letter (A-Z) |
| Allowed characters | Letters (a-z, A-Z), numbers (0-9), underscores (_) |
| Disallowed | Spaces, special characters, accented letters |
| Uniqueness | Enforced server-side by Mojang |

**Note:** This tool generates syntactically valid username candidates. It does **not** check whether a name is actually available. Use [NameMC](https://namemc.com) to check availability.

## Installation

```bash
git clone https://github.com/PeleaRaul/MCUsernameGenerator.git
cd MCUsernameGenerator
pip install -r requirements.txt
```

## Usage

```bash
python minecraft_username_generator.py
```

The GUI launches with no arguments. Configure your settings on the left panel and click **GENERATE**.

## Example Output (Realistic Mode)

```
  1.  Andrew123
  2.  sarah456
  3.  Mike_99
  4.  Emma7
  5.  alexis8204
  6.  Zachary0
  7.  anthony5786
  8.  Mia_5
```

## Tech Stack

- **Language:** Python 3
- **GUI:** CustomTkinter
- **Theme:** Dark green cyber-console (shared family)

## License

MIT
