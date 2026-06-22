# Mad libs is a game where you guess what word it would be for the next sentence
# This program will only take user inputs alone for this.

import random # essentaial to randomise the placements of certain language techniques.


# Verse 1
print("Chapter 1: The Mountain")
d1 = input("Determiner (e.g., the, a, this): ").strip()
adj1 = input("Nature Adjective (e.g., silent, frosted): ").strip()
n1 = input("Nature Noun (e.g., blossom, pine): ").strip()
p1 = input("Pronoun (e.g., it, they): ").strip()
v1 = input("Present Verb (e.g., sways, falls): ").strip()
adv1 = input("Adverb (e.g., softly, fiercely): ").strip()

# Stores 3 entirely different formats in a list, as a paragraph/verse
templates_1 = [
    f"{d1.capitalize()} {adj1} {n1},\n{p1.capitalize()} {v1} {adv1} in wind,\nSnow upon the peak.",
    f"Beneath {d1} pale moon,\n{p1.capitalize()} will {v1} {adv1} today,\n{adj1.capitalize()} {n1} rests.",
    f"{adv1.capitalize()}, {p1} {v1} now,\n{d1.capitalize()} {adj1} {n1} awakes,\nSpring is almost here."
]


# random.choice() picks one of the strings from the list above
chosen_verse_1 = random.choice(templates_1)

# Saves this to show the end result
print("\nVerse 1")
print(chosen_verse_1)
print()


# Verse 2
print("Chapter 2: The Pond")
d2 = input("Determiner: ").strip()
adj2 = input("Adjective: ").strip()
n2 = input("Noun: ").strip()
p2 = input("Pronoun: ").strip()
v2 = input("Past-Tense Verb (e.g., jumped, slept): ").strip()
adv2 = input("Adverb: ").strip()

templates_2 = [
    f"Old {adj2} {n2} sleeps,\n{d2.capitalize()} frog {v2} {adv2} inside,\nWater makes no sound.",
    f"{d2.capitalize()} frog {v2} {adv2},\n{p2.capitalize()} disturbs the {adj2} {n2},\nRipples fade away.",
    f"{adv2.capitalize()}, {p2} {v2} near,\n{d2.capitalize()} {adj2} {n2} waits below,\nQuiet lotus leaf."
]

chosen_verse_2 = random.choice(templates_2)

print("\nVerse 2")
print(chosen_verse_2)
print()

# Verse 3
print("Part 3: The Temple")
d3 = input("Determiner: ").strip()
adj3 = input("Adjective: ").strip()
n3 = input("Noun: ").strip()
p3 = input("Pronoun: ").strip()
v3 = input("Verb (e.g., bow, fade): ").strip()
adv3 = input("Adverb: ").strip()

templates_3 = [
    f"{d3.capitalize()} {adj3} {n3} fades,\n{p3.capitalize()} must {v3} {adv3} alone,\nAutumn leaves drift down.",
    f"Through {d3} {adj3} {n3},\n{p3.capitalize()} {v3} {adv3} tonight,\nLanterns glow so bright.",
    f"{adv3.capitalize()} {p3} {v3},\nBy {d3} {adj3} {n3} we rest,\nPeace is found at last."
]

chosen_verse_3 = random.choice(templates_3)

print("\nVerse 3")
print(chosen_verse_3)
print()


# Haiku Poetry

print("\n=======================")
print("    A Beautiful Scene    ")
print("=======================\n")

print(chosen_verse_1)
print()
print(chosen_verse_2)
print()
print(chosen_verse_3)