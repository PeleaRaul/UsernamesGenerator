#!/usr/bin/env python3
"""
Minecraft Username Generator v2
================================
A companion app to CyberScan Suite and ProxyScraper v3.
Generates random, syntactically valid Minecraft Java Edition usernames.

v2 adds REALISTIC MODE: uses a built-in database of 600+ real first names
to produce usernames like Andrew123, sarah456, Mike_99.

Minecraft Java Username Rules:
  - 3 to 16 characters long
  - Only letters (a-z, A-Z), numbers (0-9), and underscores (_)
  - First character must be a letter
  - Unique on the server side (this tool generates candidates, not guaranteed-available names)

Theme: Dark green cyber-console (shared with CyberScan Suite & ProxyScraper v3)
"""

import math
import random
import json
import re
import string
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

try:
    import customtkinter as ctk
except ImportError:
    print("CustomTkinter is not installed. Install with: pip install customtkinter")
    raise SystemExit(1)

# ──────────────────────────────────────────────
#  THEME — shared with CyberScan Suite / ProxyScraper v3
# ──────────────────────────────────────────────
THEME = {
    "bg":        "#070b07",
    "panel":     "#0d1410",
    "panel_lt":  "#121b14",
    "green":     "#39ff88",
    "green_dim": "#1e8a4a",
    "muted":     "#7cb895",
    "red":       "#ff4458",
    "yellow":    "#ffc944",
    "blue":      "#44aaff",
    "purple":    "#aa66ff",
    "text":      "#e0f0e6",
    "text_dim":  "#5a7a65",
    "border":    "#1a2a1e",
}

# ──────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────
MIN_LEN = 3
MAX_LEN = 16
MIN_QTY = 1
MAX_QTY = 50000
DEFAULT_QTY = 100
DEFAULT_MIN_L = 5
DEFAULT_MAX_L = 12
LETTERS = list(string.ascii_uppercase)

# Regex for final validation
RE_NO_UNDER = re.compile(r"^[A-Za-z][A-Za-z0-9]{2,15}$")
RE_WITH_UNDER = re.compile(r"^[A-Za-z][A-Za-z0-9_]{2,15}$")

# ──────────────────────────────────────────────
#  FIRST NAMES DATABASE — 600+ real names, A-Z
# ──────────────────────────────────────────────
FIRST_NAMES_BY_LETTER: dict[str, list[str]] = {
    "A": [
        "Aaron", "Abel", "Abigail", "Adam", "Adeline", "Adrian", "Aiden",
        "Alan", "Albert", "Alex", "Alexa", "Alexander", "Alexis", "Alice",
        "Allison", "Amanda", "Amber", "Amelia", "Amy", "Andrew", "Angela",
        "Angel", "Anne", "Annie", "Anthony", "April", "Archer", "Archie",
        "Ariel", "Arthur", "Asher", "Ashley", "Ashton", "Aubrey", "Audrey",
        "Austin", "Autumn", "Ava", "Avery", "Axel", "Ayden",
    ],
    "B": [
        "Barbara", "Barry", "Beatrice", "Bella", "Ben", "Benjamin",
        "Bennett", "Beth", "Bethany", "Betty", "Bianca", "Bill", "Blake",
        "Blair", "Bonnie", "Braden", "Bradley", "Brady", "Brandon",
        "Brendan", "Brett", "Brian", "Brianna", "Brooke", "Bruce", "Bryan",
        "Bryson", "Buddy",
    ],
    "C": [
        "Caleb", "Callie", "Cameron", "Camila", "Camille", "Carl", "Carla",
        "Carlos", "Carrie", "Carter", "Casey", "Cassandra", "Catherine",
        "Cecilia", "Charles", "Charlotte", "Chase", "Chelsea", "Chester",
        "Chloe", "Chris", "Christian", "Christina", "Christine",
        "Christopher", "Cindy", "Claire", "Clara", "Clayton", "Clifford",
        "Clifton", "Clinton", "Clive", "Cody", "Colby", "Cole", "Colin",
        "Connor", "Cooper", "Cora", "Corey", "Craig", "Crystal", "Curtis",
        "Cynthia",
    ],
    "D": [
        "Daisy", "Dakota", "Dallas", "Dalton", "Damian", "Damien", "Daniel",
        "Danielle", "Danny", "Darcy", "Darren", "Daryl", "David", "Dawn",
        "Dean", "Declan", "Delaney", "Dennis", "Derek", "Desmond", "Devin",
        "Dexter", "Diana", "Diane", "Dirk", "Dixon", "Dominic", "Don",
        "Donald", "Donna", "Doris", "Dorothy", "Douglas", "Drew", "Dudley",
        "Dylan",
    ],
    "E": [
        "Earl", "Eddie", "Edgar", "Edith", "Edmund", "Edward", "Edwin",
        "Eileen", "Elaine", "Eleanor", "Eli", "Elias", "Elijah", "Elise",
        "Elizabeth", "Ella", "Ellen", "Ellie", "Elsie", "Emerson", "Emily",
        "Emma", "Eric", "Erica", "Erin", "Esther", "Ethan", "Eugene",
        "Eva", "Evan", "Evelyn", "Everett",
    ],
    "F": [
        "Faith", "Fanny", "Felicia", "Felix", "Fernando", "Faye", "Finn",
        "Fiona", "Fletcher", "Florence", "Floyd", "Flynn", "Ford",
        "Forrest", "Frances", "Francis", "Francisco", "Frank", "Franklin",
        "Fred", "Frederick", "Freya",
    ],
    "G": [
        "Gabriel", "Gage", "Garrett", "Gary", "Gavin", "Gene", "Geoffrey",
        "George", "Gerald", "Gilbert", "Gina", "Ginger", "Gladys", "Glen",
        "Gloria", "Gordon", "Grace", "Graham", "Grant", "Greg", "Gregory",
        "Gwen",
    ],
    "H": [
        "Hadley", "Hailey", "Hannah", "Harley", "Harper", "Harriet",
        "Harrison", "Harry", "Harvey", "Hazel", "Heath", "Heather",
        "Heidi", "Helen", "Henry", "Herbert", "Herman", "Holden", "Holly",
        "Hope", "Howard", "Hudson", "Hugh", "Hunter",
    ],
    "I": [
        "Ian", "Ibrahim", "Ida", "Imogen", "India", "Iris", "Isaac",
        "Isabel", "Isabella", "Isabelle", "Isaiah", "Ivan", "Ivy",
    ],
    "J": [
        "Jack", "Jackson", "Jacob", "Jade", "Jake", "James", "Jamie",
        "Jane", "Jared", "Jasmine", "Jason", "Jasper", "Jay", "Jayden",
        "Jean", "Jefferson", "Jenna", "Jennifer", "Jeremiah", "Jeremy",
        "Jerome", "Jerry", "Jesse", "Jessica", "Jill", "Jim", "Jimmy",
        "Joan", "Joanna", "Jocelyn", "Jodi", "Joe", "Joel", "John",
        "Jonas", "Jonathan", "Jordan", "Joseph", "Joshua", "Joy", "Joyce",
        "Judith", "Julia", "Julie", "Julian", "Justin",
    ],
    "K": [
        "Kai", "Kaitlyn", "Kayla", "Keith", "Kelly", "Kelsey", "Kendall",
        "Kenneth", "Kent", "Kevin", "Kim", "Kimberly", "Kirk", "Kyle",
        "Kylie",
    ],
    "L": [
        "Landon", "Larry", "Laura", "Lauren", "Laurence", "Lawrence",
        "Leah", "Lee", "Leo", "Leon", "Leonard", "Leroy", "Leslie",
        "Lester", "Levi", "Lewis", "Liam", "Lillian", "Lily", "Linda",
        "Lionel", "Logan", "Lois", "Lola", "Lorena", "Lorraine", "Louis",
        "Louise", "Lucas", "Lucy", "Luke", "Luther", "Lynda", "Lydia",
        "Lyla",
    ],
    "M": [
        "Mae", "Maggie", "Malcolm", "Mallory", "Marcus", "Margaret",
        "Maria", "Mariah", "Marilyn", "Mark", "Marlene", "Marsha",
        "Marshall", "Martha", "Martin", "Marvin", "Mary", "Mason",
        "Matilda", "Matthew", "Maureen", "Max", "Maxwell", "Maya", "Megan",
        "Mel", "Melanie", "Melinda", "Melissa", "Mia", "Michael",
        "Michelle", "Mike", "Miles", "Millie", "Milton", "Molly", "Monica",
        "Morgan", "Morris", "Murray",
    ],
    "N": [
        "Nancy", "Naomi", "Natalie", "Nathan", "Nathaniel", "Neil", "Nelson",
        "Nicholas", "Nicole", "Nigel", "Nina", "Noah", "Norman", "Nora",
        "Norbert",
    ],
    "O": [
        "Oakley", "Odelia", "Ofelia", "Olga", "Olin", "Oliver", "Olivia",
        "Omar", "Oscar", "Osvaldo", "Otto", "Owen",
    ],
    "P": [
        "Pam", "Pamela", "Paris", "Parker", "Patrick", "Patsy", "Paula",
        "Paul", "Pauline", "Pedro", "Penny", "Percy", "Perry", "Pete",
        "Peter", "Philip", "Phoebe", "Phyllis", "Preston", "Priscilla",
    ],
    "Q": [
        "Quentin", "Quinn", "Quincy", "Qiana",
    ],
    "R": [
        "Rachel", "Ralph", "Randall", "Randy", "Ray", "Raymond", "Rebecca",
        "Reese", "Reginald", "Reid", "Reilly", "Rene", "Reuben", "Rex",
        "Rhett", "Rhonda", "Ricardo", "Richard", "Rick", "Riley", "Rita",
        "Rob", "Robert", "Roberto", "Robin", "Roderick", "Rodney", "Roger",
        "Roland", "Ron", "Ronald", "Rory", "Rosa", "Rose", "Roy", "Ruby",
        "Russell", "Ruth", "Ryan",
    ],
    "S": [
        "Sabrina", "Sadie", "Sally", "Sam", "Samantha", "Samuel", "Sandra",
        "Sandy", "Sarah", "Saul", "Scott", "Sean", "Sebastian", "Selena",
        "Selina", "Seth", "Shane", "Shannon", "Sharon", "Shaun", "Sheila",
        "Sheldon", "Sherman", "Shirley", "Sierra", "Silas", "Simon",
        "Solomon", "Sophia", "Spencer", "Stacy", "Stan", "Stanley",
        "Stella", "Stephanie", "Stephen", "Steve", "Steven", "Stewart",
        "Stuart", "Summer", "Susan", "Sydney", "Sylvester",
    ],
    "T": [
        "Tammy", "Tara", "Tatyana", "Taylor", "Ted", "Teddy", "Tessa",
        "Thaddeus", "Theresa", "Thomas", "Tia", "Tiffany", "Tim",
        "Timothy", "Tina", "Toby", "Todd", "Tom", "Tomas", "Tommy",
        "Tony", "Tracy", "Travis", "Trevor", "Tristan", "Trudy", "Tucker",
        "Tyler", "Tyson",
    ],
    "U": [
        "Ubaldo", "Ugo", "Ulric", "Ulrike", "Ulysses", "Uma", "Umar", "Una",
        "Ursula", "Uwe",
    ],
    "V": [
        "Val", "Valerie", "Vanessa", "Vaughn", "Velma", "Vera", "Veronica",
        "Vicki", "Victor", "Victoria", "Vince", "Vincent", "Viola",
        "Violet", "Virgil", "Virginia", "Vivian", "Vladimir",
    ],
    "W": [
        "Wade", "Walt", "Walter", "Wanda", "Warren", "Wayne", "Wendell",
        "Wendy", "Werner", "Wesley", "Whitney", "Wilbur", "William",
        "Willie", "Wilma", "Winston", "Wolfgang", "Woodrow", "Wyatt",
    ],
    "X": [
        "Xavier", "Xena", "Ximena", "Xochitl",
    ],
    "Y": [
        "Yannick", "Yasmin", "Yolanda", "Yvette", "Yvonne", "Yuki",
    ],
    "Z": [
        "Zachary", "Zachariah", "Zane", "Zara", "Zeke", "Zelda", "Zoe",
        "Zora",
    ],
}

# Flatten for quick count
_TOTAL_NAMES = sum(len(v) for v in FIRST_NAMES_BY_LETTER.values())


# ──────────────────────────────────────────────
#  USERNAME GENERATOR
# ──────────────────────────────────────────────
class UsernameGenerator:
    """Core username generation logic — no UI dependency."""

    # ── Random mode (original) ────────────────

    @staticmethod
    def generate_random(start_letter: str, min_len: int, max_len: int,
                        allow_underscores: bool, allow_numbers: bool) -> str:
        """Generate a single random alphanumeric username."""
        length = random.randint(min_len, max_len)
        if length < 1:
            length = MIN_LEN

        first = start_letter
        remaining = length - 1

        pool = string.ascii_letters
        if allow_numbers:
            pool += string.digits
        if allow_underscores:
            pool += "_"

        chars = []
        for _ in range(remaining):
            ch = random.choice(pool)
            if ch == "_" and chars and chars[-1] == "_":
                ch = random.choice(
                    string.ascii_letters + (string.digits if allow_numbers else "")
                )
            chars.append(ch)

        while chars and chars[-1] == "_":
            chars[-1] = random.choice(
                string.ascii_letters + (string.digits if allow_numbers else "")
            )

        return first + "".join(chars)

    # ── Realistic mode (new) ───────────────────

    @staticmethod
    def _pick_name(start_letter: str, min_len: int, max_len: int,
                   can_pad: bool) -> str | None:
        """
        Pick a real first name starting with the letter.
        If can_pad (numbers/underscores available), any name <= max_len works.
        If not can_pad, the name itself must be >= min_len and <= max_len.
        """
        names = FIRST_NAMES_BY_LETTER.get(start_letter.upper(), [])
        if can_pad:
            fitting = [n for n in names if len(n) <= max_len]
        else:
            fitting = [n for n in names if min_len <= len(n) <= max_len]
        if not fitting:
            for n in sorted(names, key=len):
                if len(n) >= MIN_LEN:
                    return n[:max_len]
            return None
        return random.choice(fitting)

    @staticmethod
    def _apply_case(name: str) -> str:
        """Randomly vary the case of a name for realism."""
        style = random.choice(["original", "lower", "lower", "upper_first"])
        if style == "lower":
            return name.lower()
        elif style == "upper_first":
            return name[0].upper() + name[1:].lower()
        return name  # original casing

    @staticmethod
    def _make_suffix(min_len: int, max_len: int, name_len: int,
                     allow_underscores: bool, allow_numbers: bool) -> str:
        """
        Build a suffix (numbers, optional underscore separator) that keeps
        total length within [min_len, max_len].
        """
        remaining_max = max_len - name_len
        remaining_min = max(0, min_len - name_len)

        if remaining_max <= 0:
            return ""

        parts = []

        # Sometimes add underscore separator (if allowed)
        use_under = allow_underscores and random.random() < 0.3 and remaining_max >= 2
        if use_under:
            parts.append("_")
            remaining_max -= 1

        # Add numbers if allowed
        if allow_numbers and remaining_max >= 1:
            # Decide how many digits
            max_digits = remaining_max
            # Weight toward shorter suffixes for realism
            if max_digits >= 4:
                num_digits = random.choices([1, 2, 3, 4], weights=[30, 35, 25, 10])[0]
            elif max_digits == 3:
                num_digits = random.choices([1, 2, 3], weights=[35, 40, 25])[0]
            elif max_digits == 2:
                num_digits = random.choices([1, 2], weights=[50, 50])[0]
            else:
                num_digits = 1

            num_digits = min(num_digits, max_digits)
            # Generate the number (allow leading zeros sometimes for style)
            if random.random() < 0.15:
                # Leading zero style like "Andrew07"
                num = random.randint(0, 10**num_digits - 1)
                num_str = str(num).zfill(num_digits)
            else:
                num = random.randint(0, 10**num_digits - 1)
                num_str = str(num)

            parts.append(num_str)

        suffix = "".join(parts)

        # Ensure we meet minimum length
        total = name_len + len(suffix)
        if total < min_len and allow_numbers and remaining_max > len(suffix):
            # Pad with more digits
            needed = min_len - total
            extra = "".join(str(random.randint(0, 9)) for _ in range(needed))
            # Insert before any trailing number
            if parts and parts[-1].isdigit():
                parts[-1] = extra + parts[-1]
            else:
                parts.append(extra)
            suffix = "".join(parts)

        return suffix

    @staticmethod
    def generate_realistic(start_letter: str, min_len: int, max_len: int,
                           allow_underscores: bool, allow_numbers: bool) -> str:
        """
        Generate a single realistic username using a real first name.
        Examples: Andrew123, sarah456, Mike_99, Emma7
        """
        can_pad = allow_numbers or allow_underscores
        name = UsernameGenerator._pick_name(start_letter, min_len, max_len, can_pad)
        if name is None:
            # Fallback to random mode if no names available
            return UsernameGenerator.generate_random(
                start_letter, min_len, max_len, allow_underscores, allow_numbers
            )

        # Apply case variation
        name = UsernameGenerator._apply_case(name)

        # Build suffix
        suffix = UsernameGenerator._make_suffix(
            min_len, max_len, len(name), allow_underscores, allow_numbers
        )

        result = name + suffix

        # Final validation — if something went wrong, fall back
        if not (MIN_LEN <= len(result) <= MAX_LEN):
            result = name[:max_len]
            if len(result) < MIN_LEN:
                result = name + str(random.randint(0, 9)) * (MIN_LEN - len(name))

        return result

    # ── Batch generation ──────────────────────

    @staticmethod
    def generate_batch(start_letter: str, min_len: int, max_len: int,
                       allow_underscores: bool, allow_numbers: bool,
                       quantity: int, unique: bool = True,
                       mode: str = "realistic") -> list:
        """
        Generate `quantity` usernames.
        mode: 'realistic' uses real names, 'random' uses pure random chars.
        """
        gen_fn = (UsernameGenerator.generate_realistic if mode == "realistic"
                  else UsernameGenerator.generate_random)

        if not unique:
            return [gen_fn(start_letter, min_len, max_len,
                          allow_underscores, allow_numbers)
                    for _ in range(quantity)]

        # Case-insensitive uniqueness
        results: dict[str, str] = {}  # lowercase -> original
        max_retries = quantity * 100
        retries = 0

        while len(results) < quantity and retries < max_retries:
            name = gen_fn(start_letter, min_len, max_len,
                         allow_underscores, allow_numbers)
            key = name.lower()
            if key not in results:
                results[key] = name
            retries += 1

        return list(results.values())

    @staticmethod
    def estimate_pool(start_letter: str, min_len: int, max_len: int,
                      allow_underscores: bool, allow_numbers: bool,
                      mode: str = "realistic") -> int:
        """Rough estimate of maximum unique usernames possible."""
        if mode == "random":
            pool_size = 52  # letters
            if allow_numbers:
                pool_size += 10
            if allow_underscores:
                pool_size += 1
            total = 0
            for length in range(min_len, max_len + 1):
                total += pool_size ** (length - 1)
            return total
        else:
            # Realistic: names * possible suffixes
            names = FIRST_NAMES_BY_LETTER.get(start_letter.upper(), [])
            fitting_names = [n for n in names if len(n) <= max_len]
            if not fitting_names:
                return 0

            # For each name length, estimate suffix combinations
            total = 0
            for name in fitting_names:
                name_len = len(name)
                remaining = max_len - name_len
                if remaining <= 0:
                    # Just the name itself (1 combo, but case variations ~3)
                    total += 3
                    continue
                # Estimate: ~3 case styles * (10^remaining possible numbers)
                # but cap to avoid absurd numbers
                suffix_combos = 0
                for d in range(1, remaining + 1):
                    suffix_combos += 10 ** d
                # Add no-suffix option
                suffix_combos += 1
                # Multiply by case variations (approx 3)
                total += suffix_combos * 3
            return total


# ──────────────────────────────────────────────
#  GUI
# ──────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.title("MC Username Generator v2")
        self.geometry("920x740")
        self.minsize(820, 620)
        self.configure(fg_color=THEME["bg"])

        # State
        self._generated: list[str] = []
        self._generating = False

        self._build_ui()

    # ─── UI Construction ─────────────────────────

    def _build_ui(self):
        # ── Header bar ──
        header = ctk.CTkFrame(self, fg_color=THEME["panel"], height=52,
                              corner_radius=0, border_width=0)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        title_lbl = ctk.CTkLabel(
            header, text="MC Username Generator",
            font=ctk.CTkFont(family="Consolas", size=20, weight="bold"),
            text_color=THEME["green"]
        )
        title_lbl.pack(side="left", padx=20)

        subtitle_lbl = ctk.CTkLabel(
            header, text=f"v2 · {_TOTAL_NAMES}+ real names · random & realistic modes",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=THEME["text_dim"]
        )
        subtitle_lbl.pack(side="left", padx=(0, 20))

        btn_export = ctk.CTkButton(
            header, text="Export", width=100, height=30,
            fg_color=THEME["panel_lt"], hover_color=THEME["green_dim"],
            border_color=THEME["border"], border_width=1,
            text_color=THEME["muted"],
            font=ctk.CTkFont(family="Consolas", size=12),
            command=self._on_export
        )
        btn_export.pack(side="right", padx=(5, 10), pady=10)

        btn_copy = ctk.CTkButton(
            header, text="Copy All", width=90, height=30,
            fg_color=THEME["panel_lt"], hover_color=THEME["green_dim"],
            border_color=THEME["border"], border_width=1,
            text_color=THEME["muted"],
            font=ctk.CTkFont(family="Consolas", size=12),
            command=self._on_copy
        )
        btn_copy.pack(side="right", padx=5, pady=10)

        # ── Main layout ──
        body = ctk.CTkFrame(self, fg_color=THEME["bg"], corner_radius=0)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(1, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # ── Left control panel ──
        left = ctk.CTkFrame(body, fg_color=THEME["panel"], width=310,
                            corner_radius=0)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 1))
        left.grid_propagate(False)

        self._build_controls(left)

        # ── Right results panel ──
        right = ctk.CTkFrame(body, fg_color=THEME["bg"], corner_radius=0)
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_rowconfigure(1, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self._build_results(right)

    def _build_controls(self, parent):
        pad_x = 16

        # ── Mode selector ──
        self._section_label(parent, "GENERATION MODE", pad_x, 12)

        self.mode_var = ctk.StringVar(value="realistic")
        mode_frame = ctk.CTkFrame(parent, fg_color="transparent")
        mode_frame.pack(fill="x", padx=pad_x, pady=(0, 8))

        rb_realistic = ctk.CTkRadioButton(
            mode_frame, text="Realistic Names", variable=self.mode_var,
            value="realistic",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["green"],
            fg_color=THEME["green"],
            hover_color=THEME["muted"],
            command=self._on_mode_change
        )
        rb_realistic.pack(anchor="w", pady=(0, 2))

        rb_random = ctk.CTkRadioButton(
            mode_frame, text="Random Chars", variable=self.mode_var,
            value="random",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["muted"],
            fg_color=THEME["green"],
            hover_color=THEME["muted"],
            command=self._on_mode_change
        )
        rb_random.pack(anchor="w")

        mode_hint = ctk.CTkLabel(
            parent, text="Realistic: Andrew123, sarah456\nRandom: aXk9pLm2",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=THEME["text_dim"], justify="left"
        )
        mode_hint.pack(anchor="w", padx=pad_x, pady=(0, 8))

        # ── Starting Letter ──
        self._section_label(parent, "STARTING LETTER", pad_x, 4)

        letter_frame = ctk.CTkFrame(parent, fg_color="transparent")
        letter_frame.pack(fill="x", padx=pad_x, pady=(0, 4))

        self.letter_var = ctk.StringVar(value="A")
        letter_menu = ctk.CTkOptionMenu(
            letter_frame, variable=self.letter_var,
            values=LETTERS,
            width=80, height=34,
            fg_color=THEME["panel_lt"],
            button_color=THEME["green_dim"],
            button_hover_color=THEME["green"],
            text_color=THEME["green"],
            dropdown_fg_color=THEME["panel_lt"],
            dropdown_hover_color=THEME["green_dim"],
            dropdown_text_color=THEME["text"],
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            dropdown_font=ctk.CTkFont(family="Consolas", size=14),
        )
        letter_menu.pack(side="left")

        # Show available name count for selected letter
        self.name_count_var = ctk.StringVar(
            value=f"{len(FIRST_NAMES_BY_LETTER['A'])} names"
        )
        name_count_lbl = ctk.CTkLabel(
            letter_frame, textvariable=self.name_count_var,
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=THEME["purple"]
        )
        name_count_lbl.pack(side="left", padx=(10, 0))

        rand_btn = ctk.CTkButton(
            letter_frame, text="Random", width=80, height=34,
            fg_color=THEME["panel_lt"], hover_color=THEME["green_dim"],
            border_color=THEME["border"], border_width=1,
            text_color=THEME["muted"],
            font=ctk.CTkFont(family="Consolas", size=11),
            command=self._random_letter
        )
        rand_btn.pack(side="right")

        hint = ctk.CTkLabel(
            parent, text="First char is always this letter",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=THEME["text_dim"]
        )
        hint.pack(anchor="w", padx=pad_x, pady=(0, 8))

        # ── Username Length ──
        self._section_label(parent, "USERNAME LENGTH", pad_x, 4)

        len_frame = ctk.CTkFrame(parent, fg_color="transparent")
        len_frame.pack(fill="x", padx=pad_x, pady=(0, 2))

        self.min_len_var = ctk.IntVar(value=DEFAULT_MIN_L)
        self.max_len_var = ctk.IntVar(value=DEFAULT_MAX_L)

        self.min_len_lbl = ctk.CTkLabel(
            len_frame, text=f"Min: {DEFAULT_MIN_L}",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["blue"], width=60
        )
        self.min_len_lbl.pack(side="left")

        min_slider = ctk.CTkSlider(
            len_frame, from_=MIN_LEN, to=MAX_LEN,
            variable=self.min_len_var,
            width=160, height=18,
            button_color=THEME["green"],
            button_hover_color=THEME["muted"],
            progress_color=THEME["green_dim"],
            command=self._on_min_len
        )
        min_slider.pack(side="left", padx=(4, 0))
        min_slider.set(DEFAULT_MIN_L)

        len_frame2 = ctk.CTkFrame(parent, fg_color="transparent")
        len_frame2.pack(fill="x", padx=pad_x, pady=(2, 0))

        self.max_len_lbl = ctk.CTkLabel(
            len_frame2, text=f"Max: {DEFAULT_MAX_L}",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["blue"], width=60
        )
        self.max_len_lbl.pack(side="left")

        max_slider = ctk.CTkSlider(
            len_frame2, from_=MIN_LEN, to=MAX_LEN,
            variable=self.max_len_var,
            width=160, height=18,
            button_color=THEME["green"],
            button_hover_color=THEME["muted"],
            progress_color=THEME["green_dim"],
            command=self._on_max_len
        )
        max_slider.pack(side="left", padx=(4, 0))
        max_slider.set(DEFAULT_MAX_L)

        len_hint = ctk.CTkLabel(
            parent, text="Minecraft allows 3–16 characters",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=THEME["text_dim"]
        )
        len_hint.pack(anchor="w", padx=pad_x, pady=(2, 10))

        # ── Character Options ──
        self._section_label(parent, "CHARACTERS", pad_x, 4)

        self.allow_numbers_var = ctk.BooleanVar(value=True)
        num_switch = ctk.CTkSwitch(
            parent, text="Allow numbers (0-9)",
            variable=self.allow_numbers_var,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["text"],
            progress_color=THEME["green_dim"],
            button_color=THEME["green"],
            button_hover_color=THEME["muted"],
        )
        num_switch.pack(anchor="w", padx=pad_x, pady=(0, 4))

        self.allow_underscores_var = ctk.BooleanVar(value=False)
        us_switch = ctk.CTkSwitch(
            parent, text="Allow underscores (_)",
            variable=self.allow_underscores_var,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["text"],
            progress_color=THEME["green_dim"],
            button_color=THEME["green"],
            button_hover_color=THEME["muted"],
        )
        us_switch.pack(anchor="w", padx=pad_x, pady=(0, 4))

        self.unique_var = ctk.BooleanVar(value=True)
        uniq_switch = ctk.CTkSwitch(
            parent, text="Unique only (no duplicates)",
            variable=self.unique_var,
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["text"],
            progress_color=THEME["green_dim"],
            button_color=THEME["green"],
            button_hover_color=THEME["muted"],
        )
        uniq_switch.pack(anchor="w", padx=pad_x, pady=(0, 10))

        # ── Quantity ──
        self._section_label(parent, "QUANTITY", pad_x, 4)

        qty_frame = ctk.CTkFrame(parent, fg_color="transparent")
        qty_frame.pack(fill="x", padx=pad_x, pady=(0, 2))

        self.qty_var = ctk.IntVar(value=DEFAULT_QTY)
        self.qty_lbl = ctk.CTkLabel(
            qty_frame, text=f"{DEFAULT_QTY:,}",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=THEME["yellow"], width=90
        )
        self.qty_lbl.pack(side="left")

        qty_slider = ctk.CTkSlider(
            qty_frame, from_=MIN_QTY, to=10000,
            variable=self.qty_var,
            width=140, height=18,
            button_color=THEME["green"],
            button_hover_color=THEME["muted"],
            progress_color=THEME["green_dim"],
            command=self._on_qty
        )
        qty_slider.pack(side="left", padx=(4, 0))
        qty_slider.set(DEFAULT_QTY)

        custom_frame = ctk.CTkFrame(parent, fg_color="transparent")
        custom_frame.pack(fill="x", padx=pad_x, pady=(4, 2))

        ctk.CTkLabel(
            custom_frame, text="Custom qty:",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=THEME["text_dim"]
        ).pack(side="left")

        self.qty_entry = ctk.CTkEntry(
            custom_frame, width=90, height=28,
            fg_color=THEME["panel_lt"],
            border_color=THEME["border"],
            text_color=THEME["text"],
            font=ctk.CTkFont(family="Consolas", size=12),
            placeholder_text="e.g. 25000"
        )
        self.qty_entry.pack(side="left", padx=(6, 0))
        self.qty_entry.bind("<Return>", lambda e: self._on_custom_qty())

        qty_hint = ctk.CTkLabel(
            parent, text=f"Slider: 1–10,000  |  Custom: up to {MAX_QTY:,}",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color=THEME["text_dim"]
        )
        qty_hint.pack(anchor="w", padx=pad_x, pady=(2, 12))

        # ── Generate / Clear buttons ──
        self.gen_btn = ctk.CTkButton(
            parent, text="⚡ GENERATE",
            height=42,
            fg_color=THEME["green_dim"],
            hover_color=THEME["green"],
            text_color=THEME["bg"],
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            corner_radius=8,
            command=self._on_generate
        )
        self.gen_btn.pack(fill="x", padx=pad_x, pady=(0, 6))

        self.clear_btn = ctk.CTkButton(
            parent, text="Clear Results",
            height=32,
            fg_color=THEME["panel_lt"], hover_color=THEME["green_dim"],
            border_color=THEME["border"], border_width=1,
            text_color=THEME["muted"],
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=8,
            command=self._on_clear
        )
        self.clear_btn.pack(fill="x", padx=pad_x, pady=(0, 8))

        # Stats at bottom
        self.stats_frame = ctk.CTkFrame(parent, fg_color=THEME["panel_lt"],
                                        corner_radius=6)
        self.stats_frame.pack(fill="x", padx=pad_x, pady=(8, 12))

        self.stats_lbl = ctk.CTkLabel(
            self.stats_frame, text="Generated: 0",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color=THEME["muted"],
            justify="left"
        )
        self.stats_lbl.pack(anchor="w", padx=10, pady=8)

        footer = ctk.CTkLabel(
            parent,
            text="Companion to CyberScan Suite & ProxyScraper v3",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color=THEME["text_dim"]
        )
        footer.pack(side="bottom", pady=(0, 8))

    def _build_results(self, parent):
        bar = ctk.CTkFrame(parent, fg_color=THEME["panel"], height=38,
                          corner_radius=0)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        self.results_count_lbl = ctk.CTkLabel(
            bar, text="Results: 0",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color=THEME["green"]
        )
        self.results_count_lbl.pack(side="left", padx=16)

        self.status_lbl = ctk.CTkLabel(
            bar, text="Ready",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=THEME["text_dim"]
        )
        self.status_lbl.pack(side="right", padx=16)

        self.textbox = ctk.CTkTextbox(
            parent,
            fg_color=THEME["panel"],
            text_color=THEME["text"],
            font=ctk.CTkFont(family="Consolas", size=14),
            corner_radius=0,
            wrap="none",
            border_width=0,
        )
        self.textbox.pack(fill="both", expand=True, padx=0, pady=0)
        self.textbox.configure(state="disabled")

        self._set_placeholder()

    # ─── Helpers ─────────────────────────────────

    def _section_label(self, parent, text, pad_x, pad_top):
        ctk.CTkLabel(
            parent, text=text,
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            text_color=THEME["muted"]
        ).pack(anchor="w", padx=pad_x, pady=(pad_top, 4))

    def _set_placeholder(self):
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0",
            "═══════════════════════════════════════\n"
            "  MC Username Generator v2\n"
            f"  {_TOTAL_NAMES}+ real first names built-in\n"
            "═══════════════════════════════════════\n\n"
            "  MODES:\n"
            "    Realistic — real names + numbers\n"
            "      e.g. Andrew123, sarah456, Mike_99\n\n"
            "    Random — pure random alphanumeric\n"
            "      e.g. aXk9pLm2, Bq7wRz\n\n"
            "  Configure settings on the left panel:\n"
            "    • Choose mode (Realistic / Random)\n"
            "    • Pick starting letter (A–Z)\n"
            "    • Set username length range\n"
            "    • Toggle numbers / underscores\n"
            "    • Set quantity (slider or custom)\n\n"
            "  Then click GENERATE.\n\n"
            "  Rules enforced:\n"
            "    ✓ Length: 3–16 characters\n"
            "    ✓ First char: always a letter\n"
            "    ✓ Chars: letters + numbers (+ optional _)\n"
            "    ✓ Unique mode is case-insensitive\n\n"
            "  Note: Does NOT check name availability.\n"
            "  Use NameMC for that.\n"
        )
        self.textbox.configure(state="disabled")

    def _random_letter(self):
        letter = random.choice(LETTERS)
        self.letter_var.set(letter)
        self._update_name_count(letter)

    def _update_name_count(self, letter: str):
        count = len(FIRST_NAMES_BY_LETTER.get(letter, []))
        self.name_count_var.set(f"{count} names")

    def _on_mode_change(self):
        pass  # UI updates on generate

    def _on_min_len(self, val):
        v = int(val)
        if v > self.max_len_var.get():
            self.max_len_var.set(v)
            self.max_len_lbl.configure(text=f"Max: {v}")
        self.min_len_lbl.configure(text=f"Min: {v}")

    def _on_max_len(self, val):
        v = int(val)
        if v < self.min_len_var.get():
            self.min_len_var.set(v)
            self.min_len_lbl.configure(text=f"Min: {v}")
        self.max_len_lbl.configure(text=f"Max: {v}")

    def _on_qty(self, val):
        v = int(val)
        self.qty_lbl.configure(text=f"{v:,}")
        self.qty_entry.delete(0, "end")

    def _on_custom_qty(self):
        raw = self.qty_entry.get().strip()
        if not raw:
            return
        try:
            v = int(raw)
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid number.")
            return
        v = max(MIN_QTY, min(v, MAX_QTY))
        self.qty_var.set(v)
        self.qty_lbl.configure(text=f"{v:,}")

    # ─── Generate ────────────────────────────────

    def _on_generate(self):
        if self._generating:
            return

        start_letter = self.letter_var.get()
        min_len = self.min_len_var.get()
        max_len = self.max_len_var.get()
        allow_underscores = self.allow_underscores_var.get()
        allow_numbers = self.allow_numbers_var.get()
        unique = self.unique_var.get()
        mode = self.mode_var.get()

        # Update name count display
        self._update_name_count(start_letter)

        # Custom qty
        custom = self.qty_entry.get().strip()
        if custom:
            try:
                qty = max(MIN_QTY, min(int(custom), MAX_QTY))
            except ValueError:
                qty = self.qty_var.get()
        else:
            qty = self.qty_var.get()

        # Validate
        if min_len < MIN_LEN or max_len > MAX_LEN:
            messagebox.showerror("Range Error",
                f"Length must be between {MIN_LEN} and {MAX_LEN}.")
            return
        if min_len > max_len:
            messagebox.showerror("Range Error",
                "Minimum length cannot exceed maximum length.")
            return

        # Pool limit warning
        if unique:
            pool = UsernameGenerator.estimate_pool(
                start_letter, min_len, max_len,
                allow_underscores, allow_numbers, mode
            )
            if qty > pool:
                messagebox.showwarning(
                    "Pool Limit",
                    f"With the current settings, only ~{pool:,} unique "
                    f"usernames are possible.\nYou requested {qty:,}.\n"
                    f"Reducing to {pool:,}."
                )
                qty = pool

        # UI state
        self._generating = True
        self.gen_btn.configure(state="disabled", text="⏳ Generating...")
        self.status_lbl.configure(text="Generating...", text_color=THEME["yellow"])
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        thread = threading.Thread(
            target=self._generate_worker,
            args=(start_letter, min_len, max_len,
                  allow_underscores, allow_numbers, qty, unique, mode),
            daemon=True
        )
        thread.start()

    def _generate_worker(self, start_letter, min_len, max_len,
                         allow_underscores, allow_numbers, qty, unique, mode):
        try:
            results = UsernameGenerator.generate_batch(
                start_letter, min_len, max_len,
                allow_underscores, allow_numbers, qty, unique, mode
            )
            self.after(0, lambda: self._display_results(results))
        except Exception as e:
            self.after(0, lambda: self._gen_error(str(e)))

    def _display_results(self, results):
        self._generated = results
        self._generating = False
        self.gen_btn.configure(state="normal", text="⚡ GENERATE")
        self.status_lbl.configure(text="Done", text_color=THEME["green"])

        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")

        mode_label = "Realistic" if self.mode_var.get() == "realistic" else "Random"
        header = (
            f"{'='*50}\n"
            f"  Mode: {mode_label}\n"
            f"  Generated: {len(results):,} usernames\n"
            f"  Starting letter: {self.letter_var.get()}\n"
            f"  Length: {self.min_len_var.get()}–{self.max_len_var.get()}\n"
            f"  Numbers: {'on' if self.allow_numbers_var.get() else 'off'}"
            f"  |  Underscores: {'on' if self.allow_underscores_var.get() else 'off'}\n"
            f"  Unique: {'yes' if self.unique_var.get() else 'no'}\n"
            f"  Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"{'='*50}\n\n"
        )
        self.textbox.insert("1.0", header)

        for i, name in enumerate(results, 1):
            self.textbox.insert("end", f"  {i:>5}.  {name}\n")

        self.textbox.see("1.0")
        self.textbox.configure(state="disabled")

        self.results_count_lbl.configure(text=f"Results: {len(results):,}")
        self.stats_lbl.configure(
            text=(
                f"Generated: {len(results):,}\n"
                f"Mode: {mode_label}\n"
                f"Letter: {self.letter_var.get()}\n"
                f"Length: {self.min_len_var.get()}–{self.max_len_var.get()}\n"
                f"Time: {datetime.now().strftime('%H:%M:%S')}"
            )
        )

    def _gen_error(self, msg):
        self._generating = False
        self.gen_btn.configure(state="normal", text="⚡ GENERATE")
        self.status_lbl.configure(text=f"Error: {msg}", text_color=THEME["red"])
        messagebox.showerror("Generation Error", msg)

    # ─── Export ──────────────────────────────────

    def _on_copy(self):
        if not self._generated:
            messagebox.showinfo("Nothing to copy", "Generate usernames first.")
            return
        text = "\n".join(self._generated)
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_lbl.configure(text="Copied to clipboard!", text_color=THEME["green"])

    def _on_export(self):
        if not self._generated:
            messagebox.showinfo("Nothing to export", "Generate usernames first.")
            return
        self._show_export_dialog()

    def _show_export_dialog(self):
        """Open a modal dialog to pick export format."""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Export Usernames")
        dialog.geometry("380x440")
        dialog.resizable(False, False)
        dialog.configure(fg_color=THEME["panel"])
        dialog.transient(self)
        dialog.grab_set()
        dialog.after(10, lambda: dialog.focus_force())

        fmt_var = ctk.StringVar(value="plain")

        # ── Export button at the BOTTOM (packed first so it's always visible) ──
        def do_export():
            fmt = fmt_var.get()
            dialog.destroy()
            self._do_export_with_format(fmt)

        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(side="bottom", fill="x", padx=20, pady=(4, 16))

        ctk.CTkButton(
            btn_frame, text="Export", height=38, width=160,
            fg_color=THEME["green_dim"],
            hover_color=THEME["green"],
            text_color=THEME["bg"],
            font=ctk.CTkFont(family="Consolas", size=15, weight="bold"),
            corner_radius=8,
            command=do_export
        ).pack(side="right")

        ctk.CTkButton(
            btn_frame, text="Cancel", height=38, width=100,
            fg_color=THEME["panel_lt"],
            hover_color=THEME["green_dim"],
            border_color=THEME["border"], border_width=1,
            text_color=THEME["muted"],
            font=ctk.CTkFont(family="Consolas", size=13),
            corner_radius=8,
            command=dialog.destroy
        ).pack(side="left")

        # ── Top: title + count ──
        ctk.CTkLabel(
            dialog, text="Export Format",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color=THEME["green"]
        ).pack(pady=(16, 2))

        ctk.CTkLabel(
            dialog,
            text=f"{len(self._generated):,} usernames to export",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color=THEME["text_dim"]
        ).pack(pady=(0, 10))

        # ── Format options ──
        formats = [
            ("plain",  "Plain TXT (unaltered)",   "name1\nname2\nname3"),
            ("txt",    "TXT (with metadata)",     "# header\nname1\nname2"),
            ("csv",    "CSV",                     "index,username\n1,name1"),
            ("json",   "JSON",                    '["name1","name2"]'),
        ]

        for val, label, example in formats:
            rb = ctk.CTkRadioButton(
                dialog, text=label, variable=fmt_var, value=val,
                font=ctk.CTkFont(family="Consolas", size=12),
                text_color=THEME["text"],
                fg_color=THEME["green"],
                hover_color=THEME["muted"],
            )
            rb.pack(anchor="w", padx=40, pady=(4, 0))

            ctk.CTkLabel(
                dialog, text=example,
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color=THEME["text_dim"],
                justify="left"
            ).pack(anchor="w", padx=52, pady=(0, 6))

    def _do_export_with_format(self, fmt: str):
        """Show file dialog and write the selected format."""
        letter = self.letter_var.get()
        mode = self.mode_var.get()
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")

        ext_map = {"plain": ".txt", "txt": ".txt", "csv": ".csv", "json": ".json"}
        type_map = {
            "plain": "Plain text (*.txt)",
            "txt":   "Text with metadata (*.txt)",
            "csv":   "CSV (*.csv)",
            "json":  "JSON (*.json)",
        }

        default_name = f"mc_usernames_{mode}_{letter}_{ts}{ext_map.get(fmt, '.txt')}"

        path = filedialog.asksaveasfilename(
            defaultextension=ext_map.get(fmt, ".txt"),
            filetypes=[(type_map.get(fmt, "Text"), f"*{ext_map.get(fmt, '.txt')}"),
                       ("All files", "*.*")],
            initialfile=default_name,
        )
        if not path:
            return

        try:
            if fmt == "plain":
                with open(path, "w") as f:
                    for name in self._generated:
                        f.write(name + "\n")

            elif fmt == "txt":
                with open(path, "w") as f:
                    f.write(f"# Minecraft Username Generator v2\n")
                    f.write(f"# Mode: {mode}\n")
                    f.write(f"# Starting letter: {letter}\n")
                    f.write(f"# Length: {self.min_len_var.get()}-{self.max_len_var.get()}\n")
                    f.write(f"# Numbers: {'on' if self.allow_numbers_var.get() else 'off'}\n")
                    f.write(f"# Underscores: {'on' if self.allow_underscores_var.get() else 'off'}\n")
                    f.write(f"# Unique: {'yes' if self.unique_var.get() else 'no'}\n")
                    f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# Count: {len(self._generated)}\n")
                    f.write(f"#{'='*50}\n\n")
                    for name in self._generated:
                        f.write(name + "\n")

            elif fmt == "csv":
                with open(path, "w", newline="") as f:
                    import csv as csv_mod
                    writer = csv_mod.writer(f)
                    writer.writerow(["index", "username"])
                    for i, name in enumerate(self._generated, 1):
                        writer.writerow([i, name])

            elif fmt == "json":
                data = {
                    "generator": "MC Username Generator v2",
                    "mode": mode,
                    "starting_letter": letter,
                    "length_range": [self.min_len_var.get(), self.max_len_var.get()],
                    "numbers": self.allow_numbers_var.get(),
                    "underscores": self.allow_underscores_var.get(),
                    "unique": self.unique_var.get(),
                    "count": len(self._generated),
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "usernames": self._generated,
                }
                with open(path, "w") as f:
                    json.dump(data, f, indent=2)

            self.status_lbl.configure(
                text=f"Exported: {path.split('/')[-1]}", text_color=THEME["green"]
            )
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

    def _on_clear(self):
        self._generated = []
        self._set_placeholder()
        self.results_count_lbl.configure(text="Results: 0")
        self.stats_lbl.configure(text="Generated: 0")
        self.status_lbl.configure(text="Ready", text_color=THEME["text_dim"])


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────
def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
