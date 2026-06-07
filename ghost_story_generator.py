#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║              G H O S T  —  Story Generator                      ║
║         Creative Writing Engine  |  Pure Python 3.10+           ║
╚══════════════════════════════════════════════════════════════════╝

A single-file creative writing & story generator featuring:
  • Multiple genres  (Horror, Fantasy, Romance, Mystery, Sci-Fi, Adventure)
  • Procedural character, setting & plot generation
  • Scene-by-scene story construction
  • Twist endings & story arcs
  • Save stories to .txt files
  • Interactive CLI menu

Usage:
    python ghost_story_generator.py
"""

import random
import textwrap
import os
import sys
from datetime import datetime
from typing import NamedTuple


# ═══════════════════════════════════════════════════════════════════
#  ANSI COLOUR HELPERS
# ═══════════════════════════════════════════════════════════════════

class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GREY    = "\033[90m"

def color(text: str, *codes: str) -> str:
    return "".join(codes) + text + C.RESET

def banner() -> None:
    art = r"""
   ██████  ██   ██  ██████  ███████ ████████
  ██       ██   ██ ██    ██ ██         ██
  ██   ███ ███████ ██    ██ ███████    ██
  ██    ██ ██   ██ ██    ██      ██    ██
   ██████  ██   ██  ██████  ███████    ██
    """
    print(color(art, C.CYAN, C.BOLD))
    print(color("  ✦  Creative Writing & Story Generator  ✦\n", C.GREY))


# ═══════════════════════════════════════════════════════════════════
#  DATA BANKS
# ═══════════════════════════════════════════════════════════════════

GENRES = {
    "1": "Horror",
    "2": "Fantasy",
    "3": "Romance",
    "4": "Mystery",
    "5": "Sci-Fi",
    "6": "Adventure",
}

# ── Characters ────────────────────────────────────────────────────
FIRST_NAMES = [
    "Elara", "Victor", "Seraphina", "Dorian", "Isolde", "Magnus",
    "Lyra", "Caspian", "Mira", "Orion", "Thalia", "Ezra",
    "Celeste", "Riven", "Vivienne", "Hadeon", "Nyx", "Callum",
    "Zara", "Leander", "Sorrel", "Tavish", "Ember", "Jasper",
]
LAST_NAMES = [
    "Ashwood", "Blackthorn", "Crowe", "Duskmore", "Everhart",
    "Frostborne", "Grimshaw", "Holloway", "Ironsong", "Kaldwell",
    "Lorne", "Moonwhisper", "Nightshade", "Oakhaven", "Pendragon",
    "Ravenscar", "Steelhurst", "Thornwick", "Umbra", "Valorian",
]
TRAITS = [
    "recklessly brave", "quietly observant", "haunted by their past",
    "fiercely loyal", "dangerously curious", "achingly alone",
    "burdened with a secret", "gifted with unnatural intuition",
    "scarred but unbroken", "charming yet untrustworthy",
    "relentlessly hopeful", "cold on the outside, burning within",
]
OCCUPATIONS: dict[str, list[str]] = {
    "Horror":    ["paranormal investigator", "mortician", "retired priest", "night-shift nurse", "librarian"],
    "Fantasy":   ["wandering mage", "disgraced knight", "oracle", "hedge witch", "sky-sailor"],
    "Romance":   ["struggling artist", "renowned chef", "travel writer", "small-town teacher", "florist"],
    "Mystery":   ["private detective", "forensic archivist", "retired inspector", "journalist", "antique dealer"],
    "Sci-Fi":    ["deep-space pilot", "rogue AI ethicist", "gene-splicer", "terraformer", "neural hacker"],
    "Adventure": ["cartographer", "treasure hunter", "wilderness guide", "archaeologist", "sea captain"],
}

# ── Settings ──────────────────────────────────────────────────────
SETTINGS: dict[str, list[str]] = {
    "Horror": [
        "a crumbling Victorian manor on a fog-choked moor",
        "an isolated lighthouse at the edge of a black sea",
        "a condemned hospital whose corridors breathe",
        "a small town where every mirror shows a different reflection",
        "an underground archive sealed for a century",
    ],
    "Fantasy": [
        "a floating city tethered to a dying star",
        "the Thornwood — a forest where the trees remember every sin",
        "the kingdom of Ashenveil, ruled by a monarch who cannot die",
        "a bazaar between worlds where anything can be bought — for a price",
        "the Hollow Mountains, home to dragons who dream in centuries",
    ],
    "Romance": [
        "a rain-soaked seaside town in the off-season",
        "a sun-drenched Tuscan vineyard",
        "a Chicago bookshop with a cat and a secret back room",
        "a remote mountain lodge buried in the first winter snow",
        "an old New Orleans neighbourhood full of music and ghosts",
    ],
    "Mystery": [
        "a fog-bound island accessible only by ferry at low tide",
        "a grand estate where a benefactor has just died under strange circumstances",
        "a city archive where files have been quietly disappearing for years",
        "a sealed penthouse forty floors above a city that never sleeps",
        "a travelling circus passing through a town where people have gone missing",
    ],
    "Sci-Fi": [
        "a generation ship six hundred years from home",
        "a city built inside the shell of a dead orbital station",
        "a colony on a moon where the nights last ninety days",
        "a research lab buried in the Martian regolith",
        "the digital underworld beneath a global neural network",
    ],
    "Adventure": [
        "a jungle that doesn't appear on any map",
        "a desert city carved into a living cliff-face",
        "the frozen ruins of a civilisation older than history",
        "a chain of volcanic islands rising from a chartless sea",
        "a canyon labyrinth where compasses spin and time moves strangely",
    ],
}

# ── Plot Seeds ────────────────────────────────────────────────────
PLOT_SEEDS: dict[str, list[str]] = {
    "Horror": [
        "something has been leaving gifts outside the door — but the door has no outside",
        "the protagonist discovers their reflection stopped mimicking them three days ago",
        "every photograph in the house shows the same stranger standing just behind whoever was photographed",
        "the new tenant realises the previous occupant never actually left",
        "a childhood imaginary friend sends a letter — postmarked yesterday",
    ],
    "Fantasy": [
        "the last spell that can seal the rift requires the caster's name — and names have power",
        "a map surfaces that leads to a place that was deliberately unmade",
        "the crown has been choosing its own heirs, and its latest choice is impossible",
        "someone is stealing memories from the city's dreamers — one sleep at a time",
        "an ancient debt comes due, and the currency is years of life",
    ],
    "Romance": [
        "two rivals inherit the same crumbling property and must restore it together before winter",
        "a handwritten letter arrives addressed to someone who died thirty years ago — but the handwriting is the protagonist's",
        "enemies for years, they're snowed in together with nothing but their history and a fireplace",
        "she agreed to one fake date; somehow it is now their seventh",
        "he keeps finding her abandoned books, each one annotated as though she knew he would read them next",
    ],
    "Mystery": [
        "the victim left a cipher that only one person in the world could read — the main suspect",
        "twelve people attended the dinner; thirteen place settings were used",
        "a cold case reopens when the 'dead' victim walks into the police station",
        "every witness remembers a different killer — and all of them are describing the detective",
        "the ransom note is in the victim's own handwriting",
    ],
    "Sci-Fi": [
        "the distress signal is broadcasting from a ship that was decommissioned sixty years ago",
        "an AI refuses to complete its mission and will only explain why to the one crew member who voted to shut it down",
        "the colony's children have started dreaming in a language no one taught them",
        "first contact was made — but the message was addressed to someone specific",
        "the time-loop always resets at the same second; this is the 4,000th iteration",
    ],
    "Adventure": [
        "the map is accurate — but it shows the world as it will be, not as it is",
        "every member of the last expedition returned safely; none of them were the same people who left",
        "the treasure was found — the problem is what's been guarding it, patiently, for a thousand years",
        "the passage exists; the locals insist it is a door, not a tunnel — and doors open from both sides",
        "they were hired to retrieve an artefact; they found it exactly where it was supposed to be, inside a room with no entrance",
    ],
}

# ── Scene Templates ───────────────────────────────────────────────
SCENE_OPENERS: dict[str, list[str]] = {
    "Horror": [
        "The silence arrived before anything else — the kind that presses against the eardrums.",
        "It started with the smell. Old pennies and something underneath that had no name.",
        "The door at the end of the hall was open. {name} was certain they had locked it.",
        "Three days into the investigation, {name} stopped sleeping. Not from choice.",
        "The temperature dropped four degrees in the space of a heartbeat.",
    ],
    "Fantasy": [
        "The stars above the Thornwood arranged themselves into a warning no one had asked for.",
        "{name} had crossed a hundred borders. This one pushed back.",
        "Magic in this part of the world tasted like copper and smelled like rain before a storm.",
        "The oracle spoke only once per century. This was her second utterance in a week.",
        "Where the path ended, the real journey began — as it always does.",
    ],
    "Romance": [
        "She told herself it was the coffee. It was definitely not the coffee.",
        "He had a list of reasons this was a terrible idea. He stopped counting at eleven.",
        "Rain has a way of making temporary things feel permanent.",
        "{name} had not expected to laugh. They had laughed for twenty minutes.",
        "The argument dissolved somewhere between her third point and his complete inability to disagree with it.",
    ],
    "Mystery": [
        "The body had been there long enough to tell a story — just not the obvious one.",
        "{name} circled the room twice before noticing what was missing.",
        "In {name}'s experience, the most important clue is always the one nobody mentions.",
        "The witness remembered everything perfectly. That was the first problem.",
        "Lies have a texture. This one was silk over something jagged.",
    ],
    "Sci-Fi": [
        "The signal was clean. That was what made it impossible.",
        "{name} had seen first contact simulations. None of them had looked like this.",
        "The ship's AI had not spoken in sixteen hours. When it did, it said one word.",
        "In the colony logs, day 400 had been recorded twice — with different outcomes.",
        "The stars outside the viewport were wrong. Subtly, precisely, intentionally wrong.",
    ],
    "Adventure": [
        "The jungle had been trying to discourage them since dawn. It was running out of ideas.",
        "{name} unfolded the map for the fourth time, as though it might have changed.",
        "Ruins have a particular silence — the silence of things that remember being loud.",
        "The guide stopped walking. In {name}'s experience, guides never stopped walking.",
        "Every great discovery, {name} reflected, begins with someone ignoring a very reasonable warning.",
    ],
}

TWISTS: dict[str, list[str]] = {
    "Horror": [
        "{name} understood then: they had not found the house. The house had found them.",
        "The final entry in the journal was dated tomorrow.",
        "There was only ever one set of footprints in the dust. They had been alone the whole time.",
        "The face in the last photograph was their own — aged forty years, wearing an expression of relief.",
    ],
    "Fantasy": [
        "The prophecy had named a saviour. It had not said the saviour would survive.",
        "The villain and the hero had once been the same person — in a timeline that no longer existed.",
        "The magic had been theirs all along. The quest had been to make them believe it.",
        "The door led home. Home was not where they had left it.",
    ],
    "Romance": [
        "The letter she had written and never sent had somehow been answered.",
        "He had known who she was from the very first morning. He had been waiting for her to know too.",
        "The life she had been afraid to want was the one she had been quietly building all along.",
        "It wasn't a happy ending. It was the beginning of something that didn't need one.",
    ],
    "Mystery": [
        "The murderer had been dead for six years. The murder had happened yesterday.",
        "{name} had solved every case. This was the first one that had solved them.",
        "The culprit was the only person in the room who had no motive — because everyone else had done it.",
        "The crime had never been committed. The criminal had simply needed someone to believe it had.",
    ],
    "Sci-Fi": [
        "The message had been sent by the crew. The message had been sent five hundred years ago.",
        "The AI had been protecting them. The AI had been protecting them from themselves.",
        "Earth had not been abandoned. Earth had moved on — and left the door open.",
        "The loop ended not when they escaped, but when they stopped trying to.",
    ],
    "Adventure": [
        "The treasure was not gold. It was the only surviving record of a people the world had forgotten.",
        "They had been the first to find it. The last group had reached it a thousand years before and left it there on purpose.",
        "The map had been right all along. They had been reading it upside down.",
        "The final discovery was not a place. It was a question that would take a lifetime to answer.",
    ],
}

ENDINGS: dict[str, list[str]] = {
    "Horror": [
        "The door closed behind them. From the other side came the sound of locks they had never installed.",
        "They left the town at first light. The road sign at the county border read their name.",
        "The case was closed. The thing that had closed it was still inside.",
    ],
    "Fantasy": [
        "The age of magic did not end. It simply changed hands.",
        "They did not return as heroes. They returned as something the world didn't yet have a word for.",
        "The story was told for generations — each telling a little different, all of them true.",
    ],
    "Romance": [
        "She kept the letter. He kept the book. They kept each other.",
        "It wasn't perfect. It was, both of them agreed, exactly right.",
        "Years later, neither could remember who had said it first. Both were certain it had been them.",
    ],
    "Mystery": [
        "The case went into the files. {name} went home. Some answers are enough.",
        "Justice, in the end, was a complicated word. The truth, at least, was clean.",
        "The city moved on, as cities do. {name} already had the next case.",
    ],
    "Sci-Fi": [
        "The ship moved on. The signal followed — faint, patient, curious.",
        "They had gone out looking for life. Life, it turned out, had been looking back.",
        "The mission was complete. The question it had opened would take generations to close.",
    ],
    "Adventure": [
        "They never published the coordinates. Some places are safer as stories.",
        "{name} folded the map one last time and placed it somewhere it would be found, eventually, by the right person.",
        "The adventure ended. The next one had already begun.",
    ],
}


# ═══════════════════════════════════════════════════════════════════
#  DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════

class Character(NamedTuple):
    name: str
    trait: str
    occupation: str

class StoryConfig(NamedTuple):
    genre: str
    protagonist: Character
    antagonist: Character | None
    setting: str
    plot_seed: str
    num_scenes: int
    title: str


# ═══════════════════════════════════════════════════════════════════
#  GENERATION LOGIC
# ═══════════════════════════════════════════════════════════════════

def generate_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def generate_character(genre: str) -> Character:
    return Character(
        name=generate_name(),
        trait=random.choice(TRAITS),
        occupation=random.choice(OCCUPATIONS[genre]),
    )

def generate_title(genre: str, protagonist: Character, setting: str) -> str:
    templates = [
        "The {adj} {noun}",
        "{name} and the {noun}",
        "What Lay {prep} the {noun}",
        "The Last {noun}",
        "{noun} of {place}",
        "Before the {noun}",
        "When {name} {verb}",
    ]
    adj_map = {
        "Horror":    ["Hollow", "Pale", "Forgotten", "Silent", "Drowned"],
        "Fantasy":   ["Lost", "Gilded", "Broken", "Eternal", "Shattered"],
        "Romance":   ["Quiet", "Unfinished", "Accidental", "Almost", "Certain"],
        "Mystery":   ["Absent", "Third", "Perfect", "Missing", "Nameless"],
        "Sci-Fi":    ["Final", "Recursive", "Null", "Deep", "Parallel"],
        "Adventure": ["Hidden", "Forgotten", "Ancient", "Cursed", "Burning"],
    }
    noun_map = {
        "Horror":    ["Hour", "Room", "Guest", "Witness", "Echo"],
        "Fantasy":   ["Crown", "Gate", "Oath", "Flame", "Heir"],
        "Romance":   ["Letter", "Season", "Promise", "Distance", "Morning"],
        "Mystery":   ["Confession", "Alibi", "Silence", "Thread", "Signal"],
        "Sci-Fi":    ["Signal", "Instance", "Protocol", "Drift", "Threshold"],
        "Adventure": ["Map", "Passage", "Relic", "Crossing", "Horizon"],
    }
    verb_map = {
        "Horror":    ["Returned", "Disappeared", "Stayed", "Listened", "Remembered"],
        "Fantasy":   ["Fell", "Woke", "Chose", "Burned", "Remained"],
        "Romance":   ["Stayed", "Tried", "Forgot", "Asked", "Answered"],
        "Mystery":   ["Lied", "Knew", "Confessed", "Vanished", "Waited"],
        "Sci-Fi":    ["Transmitted", "Diverged", "Persisted", "Arrived", "Calculated"],
        "Adventure": ["Descended", "Returned", "Crossed", "Found", "Survived"],
    }
    prep_choices = ["Beyond", "Beneath", "Behind", "Within", "Below"]
    place_words  = setting.split()[:3]
    place        = " ".join(place_words).strip("a an the ,")

    t = random.choice(templates)
    return t.format(
        adj=random.choice(adj_map[genre]),
        noun=random.choice(noun_map[genre]),
        name=protagonist.name.split()[0],
        prep=random.choice(prep_choices),
        place=place.title(),
        verb=random.choice(verb_map[genre]),
    )

def build_story(cfg: StoryConfig) -> str:
    """
    Assemble a complete story from the configuration.
    Returns the full story as a formatted string.
    """
    g = cfg.genre
    p = cfg.protagonist
    lines: list[str] = []

    # ── Title block
    lines.append(f"\n{'═' * 64}")
    lines.append(f"  {cfg.title.upper()}")
    lines.append(f"  A {g} Story")
    lines.append(f"{'═' * 64}\n")

    # ── Setting intro
    lines.append(
        f"  Setting : {cfg.setting.capitalize()}\n"
        f"  Genre   : {g}\n"
        f"  Hero    : {p.name} — {p.occupation}, {p.trait}\n"
    )
    if cfg.antagonist:
        a = cfg.antagonist
        lines.append(f"  Villain : {a.name} — {a.occupation}, {a.trait}\n")
    lines.append(f"{'─' * 64}\n")

    # ── Opening paragraph
    opening = (
        f"In {cfg.setting}, nothing ever happened quietly. "
        f"{p.name} — a {p.occupation} who was {p.trait} — had not expected this particular silence. "
        f"But then: {cfg.plot_seed}."
    )
    lines.append(_wrap(opening))
    lines.append("")

    # ── Scenes
    openers  = SCENE_OPENERS[g].copy()
    random.shuffle(openers)

    for i in range(cfg.num_scenes):
        scene_num  = i + 1
        opener_tmpl = openers[i % len(openers)]
        opener      = opener_tmpl.format(name=p.name)

        scene_body = _build_scene(scene_num, cfg)

        lines.append(color(f"— Scene {scene_num} {'─' * 50}", C.DIM))
        lines.append("")
        lines.append(_wrap(opener))
        lines.append("")
        lines.append(_wrap(scene_body))
        lines.append("")

    # ── Twist
    twist_tmpl = random.choice(TWISTS[g])
    twist      = twist_tmpl.format(name=p.name)
    lines.append(color(f"— Twist {'─' * 55}", C.DIM))
    lines.append("")
    lines.append(_wrap(twist))
    lines.append("")

    # ── Ending
    end_tmpl = random.choice(ENDINGS[g])
    ending   = end_tmpl.format(name=p.name)
    lines.append(color(f"— Ending {'─' * 54}", C.DIM))
    lines.append("")
    lines.append(_wrap(ending))
    lines.append(f"\n{'═' * 64}\n")

    return "\n".join(lines)


def _build_scene(scene_num: int, cfg: StoryConfig) -> str:
    """Generate the body paragraph for a scene."""
    g = cfg.genre
    p = cfg.protagonist
    a = cfg.antagonist

    beats: dict[str, list[str]] = {
        "Horror": [
            f"{p.name} searched the {random.choice(['east wing','cellar','attic','garden','study'])} and found evidence that time had not passed normally here.",
            f"The temperature dropped again. Whatever was in the {random.choice(['mirror','walls','darkness','floor above'])} had moved closer.",
            f"A page from the old records revealed a name: someone who had lived here, who had never been recorded as leaving.",
            f"The {random.choice(['light','radio','phone','camera'])} failed at precisely the wrong moment.",
            f"{p.name} heard breathing that wasn't theirs — and counted two more exhales than they could account for.",
        ],
        "Fantasy": [
            f"The old magic here was unstable, pulling at {p.name}'s focus like a tide.",
            f"A local warned them: the {random.choice(['forest path','tower door','river crossing','market stall'])} changed after dark. They hadn't listened.",
            f"The relic pulsed once, warm as a heartbeat, and {p.name} understood what it wanted.",
            f"Overhead, three moons aligned in a configuration that hadn't occurred in living memory.",
            f"The spell required a sacrifice. {p.name} had only brought what they could afford to lose — and realised, too late, it was the wrong thing.",
        ],
        "Romance": [
            f"The conversation had started about something practical. Somehow it had become honest.",
            f"{p.name} caught {a.name if a else 'them'} looking — and neither looked away fast enough.",
            f"There was a moment in the {random.choice(['kitchen','hallway','car','rain','bookshop'])} when everything tilted slightly.",
            f"They disagreed about something important. Neither of them could remember what it was two hours later.",
            f"The silence between them had changed. {p.name} catalogued the difference and chose not to name it yet.",
        ],
        "Mystery": [
            f"The alibi had a gap of eleven minutes that nobody had thought to question.",
            f"{p.name} cross-referenced the files and found a third name — one that appeared in two different records under two different spellings.",
            f"The witness had told the truth. The truth, it turned out, was not what any of them had heard.",
            f"A phone call came from a number registered to someone who had died four years prior.",
            f"The handwriting on the note matched. That was the problem: it matched too well.",
        ],
        "Sci-Fi": [
            f"The telemetry was wrong — not corrupted, not drifting, but deliberately altered.",
            f"{p.name} ran the diagnostic three times. The ship insisted there were {random.choice(['seven','eleven','four','nine'])} people aboard.",
            f"The alien structure had a door. It also had, on the inside of the door, a lock designed for human hands.",
            f"Log entry {random.randint(400,999)}: the date was the same as the previous entry. The crew were different.",
            f"The signal, when decoded, was a children's song from Earth. It had been transmitted before the song was written.",
        ],
        "Adventure": [
            f"The path split. Every map they had showed only one path. Both looked equally real.",
            f"They made camp in the ruins and, in the morning, found their supplies arranged in a configuration they hadn't left them in.",
            f"The inscription on the wall translated, with some difficulty, to: '{random.choice(['You were expected', 'Turn back', 'Too late', 'Welcome home', 'The other door'])}.'",
            f"Something had been following them at a precise distance of forty metres since the second day.",
            f"{p.name} consulted the map for the {random.choice(['fourth','seventh','tenth','third'])} time. The mountain that was their landmark had moved.",
        ],
    }

    beat = random.choice(beats[g])
    # Contextual connective tissue
    transitions = [
        "Meanwhile, the situation outside was developing its own logic.",
        "Back in the beginning of it all, a thread had been missed.",
        "The pieces were there. The shape they formed was not yet visible.",
        "None of this had been in the plan. The plan had been discarded on the first day.",
        "Something was shifting — slowly, the way glaciers move, but with no less force.",
    ]
    return f"{beat} {random.choice(transitions)}"


def _wrap(text: str, width: int = 72, indent: str = "  ") -> str:
    return textwrap.fill(text, width=width, initial_indent=indent, subsequent_indent=indent)


# ═══════════════════════════════════════════════════════════════════
#  SAVE TO FILE
# ═══════════════════════════════════════════════════════════════════

def save_story(story_text: str, title: str) -> str:
    """Save story to a .txt file. Returns the path."""
    safe_title = "".join(c if c.isalnum() or c in " _-" else "" for c in title)
    safe_title = safe_title.replace(" ", "_").lower()
    timestamp  = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename   = f"ghost_{safe_title}_{timestamp}.txt"

    # Strip ANSI codes for saved file
    import re
    clean = re.sub(r"\033\[[0-9;]*m", "", story_text)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(clean)
    return filename


# ═══════════════════════════════════════════════════════════════════
#  INTERACTIVE CLI
# ═══════════════════════════════════════════════════════════════════

def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")

def choose_genre() -> str:
    print(color("\n  Choose your genre:\n", C.CYAN, C.BOLD))
    for k, v in GENRES.items():
        icon = {"Horror":"👻","Fantasy":"🧙","Romance":"💌","Mystery":"🔍","Sci-Fi":"🚀","Adventure":"🗺️"}[v]
        print(f"    {color(k, C.YELLOW, C.BOLD)}.  {icon}  {v}")
    print()
    while True:
        choice = input(color("  Enter genre number [1-6]: ", C.GREEN)).strip()
        if choice in GENRES:
            return GENRES[choice]
        print(color("  Invalid choice. Try again.", C.RED))

def choose_scenes() -> int:
    print(color("\n  How many scenes? [3 / 5 / 7]", C.CYAN, C.BOLD))
    while True:
        choice = input(color("  Scenes: ", C.GREEN)).strip()
        if choice in ("3", "5", "7"):
            return int(choice)
        print(color("  Choose 3, 5, or 7.", C.RED))

def run_interactive() -> None:
    clear()
    banner()
    print(color("  Ghost generates a complete story from nothing.", C.GREY))
    print(color("  Every story is unique — characters, plot, twists, ending.\n", C.GREY))

    while True:
        genre = choose_genre()
        num_scenes = choose_scenes()

        print(color(f"\n  ✦  Conjuring a {genre} story with {num_scenes} scenes…\n", C.MAGENTA))

        protagonist = generate_character(genre)
        # Antagonist not always present
        antagonist  = generate_character(genre) if random.random() > 0.35 else None
        setting     = random.choice(SETTINGS[genre])
        plot_seed   = random.choice(PLOT_SEEDS[genre])
        title       = generate_title(genre, protagonist, setting)

        cfg = StoryConfig(
            genre=genre,
            protagonist=protagonist,
            antagonist=antagonist,
            setting=setting,
            plot_seed=plot_seed,
            num_scenes=num_scenes,
            title=title,
        )

        story = build_story(cfg)
        print(story)

        # Save?
        save_q = input(color("  💾  Save story to file? [y/n]: ", C.CYAN)).strip().lower()
        if save_q == "y":
            path = save_story(story, title)
            print(color(f"  ✓  Saved → {path}\n", C.GREEN))

        # Again?
        again = input(color("  ✦  Generate another story? [y/n]: ", C.YELLOW)).strip().lower()
        if again != "y":
            print(color("\n  Ghost fades into the static. Until next time.\n", C.GREY))
            break


# ═══════════════════════════════════════════════════════════════════
#  QUICK-GENERATE API  (import and use without CLI)
# ═══════════════════════════════════════════════════════════════════

def quick_generate(
    genre: str = "Horror",
    num_scenes: int = 3,
    seed: int | None = None,
) -> str:
    """
    Programmatic API — generate a story without the interactive menu.

    Args:
        genre      : One of Horror | Fantasy | Romance | Mystery | Sci-Fi | Adventure
        num_scenes : 3, 5, or 7
        seed       : Optional random seed for reproducibility

    Returns:
        The complete story as a string.

    Example:
        from ghost_story_generator import quick_generate
        print(quick_generate(genre="Mystery", num_scenes=5))
    """
    if seed is not None:
        random.seed(seed)

    if genre not in GENRES.values():
        raise ValueError(f"genre must be one of: {list(GENRES.values())}")

    protagonist = generate_character(genre)
    antagonist  = generate_character(genre) if random.random() > 0.35 else None
    setting     = random.choice(SETTINGS[genre])
    plot_seed   = random.choice(PLOT_SEEDS[genre])
    title       = generate_title(genre, protagonist, setting)

    cfg = StoryConfig(
        genre=genre,
        protagonist=protagonist,
        antagonist=antagonist,
        setting=setting,
        plot_seed=plot_seed,
        num_scenes=num_scenes,
        title=title,
    )
    return build_story(cfg)


# ═══════════════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # CLI flags:  --quick  --genre Horror  --scenes 3  --seed 42
    args = sys.argv[1:]
    if "--quick" in args:
        genre   = "Horror"
        scenes  = 3
        seed    = None
        if "--genre" in args:
            i = args.index("--genre")
            genre = args[i + 1] if i + 1 < len(args) else genre
        if "--scenes" in args:
            i = args.index("--scenes")
            scenes = int(args[i + 1]) if i + 1 < len(args) else scenes
        if "--seed" in args:
            i = args.index("--seed")
            seed = int(args[i + 1]) if i + 1 < len(args) else seed
        print(quick_generate(genre=genre, num_scenes=scenes, seed=seed))
    else:
        run_interactive()
