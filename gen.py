x = 13
note = "A"
notes = ["E", "F", "F#", "G", "G#", "E", "D#", "F#", "G", "F#"]
mapper = {'A': 'A#', 'A#': 'B', 'B': 'C', 'C': 'C#', 'C#': 'D', 'D': 'D#', 'D#': 'E', 'E': 'F', 'F': 'F#', 'F#': 'G',
          'G': 'G#', 'G#': 'A'}


def temp():
    return f"""{x + 0} %s {x + 1} %s {x + 5}
{x + 1} %s {x + 2} %s {x + 3} %s {x + 4} {note}Mj
{x + 2} {note}Mj6
{x + 3} {note}Dom7
{x + 4} {note}Mj7
{x + 5} {note}Aug

{x + 6} %s {x + 7} %s {x + 10}
{x + 7} %s {x + 8} %s {x + 9} {note}Mn
{x + 8} {note}Mn6
{x + 9} {note}Mn7
{x + 10} %s {x + 11} {note}Dim
{x + 11} {note}Dim7"""


# while True:
#     print("--------------------" * 2)
#     print(note)
#     print(temp() % tuple(notes))
#     notes = [mapper[note] for note in notes]
#     note = mapper[note]
#     x += 12
#
#     if note == "A":
#         break

x = 1
y = 19
z = 13
n = ["C", "C#"]


def temp():
    return f"{x:0>2} %s. {y} %s. {z}"


for i in range(12):
    print(temp() % tuple(n))
    n = [mapper[note] for note in n]
    x += 1
    y += 12
    z += 12
