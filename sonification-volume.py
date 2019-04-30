import csv
import math
from midiutil.MidiFile import MIDIFile

m = MIDIFile(1)
m.addTrackName(0, 0, "LANL Login Activity")
m.addTempo(0, 0, 80)

b2 = 35
c2 = 36
d2 = 38
e2 = 40
f2 = 41
g2 = 43
a3 = 45
b4 = 59
c4 = 60
d4 = 62
e4 = 64
f4 = 65
g4 = 67
a5 = 69
b5 = 71
c5 = 72

c_arp = [ c4, e4, g4, c5 ]
f_arp = [ c4, f4, a5, c5 ]
g_arp = [ b4, d4, g4, b5 ]

pattern = c_arp + c_arp + f_arp + f_arp + g_arp + g_arp + c_arp + c_arp

c_chord = [ c2, e2, g2 ]
f_chord = [ c2, f2, a3 ]
g_chord = [ b2, d2, g2 ]

whole_note = 4.0
eighth_note = whole_note / 8.0
min_volume = 20
max_volume = 127

# first pass, find the highest value
max_value = 0
with open("quarter-hour-chunked.csv", "r") as csv_file:
	csv_reader = csv.reader(csv_file)
	for row in csv_reader:
		max_value = max(max_value, int(row[0]))
print("Maximum value from the data is: {}".format(max_value))
intervals = 4
interval_size = math.ceil(max_value / intervals)
print("We should have {} intervals of {} each".format(intervals, interval_size))

def getVolume(value):
	ratio = value / max_value
	volume_range = max_volume - min_volume
	return round(volume_range * ratio) + min_volume

# second pass, generate music
current_note = 0
beat = 0
with open("quarter-hour-chunked.csv", "r") as csv_file:
	csv_reader = csv.reader(csv_file)
	for row in csv_reader:
		value = int(row[0])
		m.addNote(0, 0, pattern[current_note], beat, eighth_note, getVolume(value))
		current_note = (current_note + 1) % len(pattern)
		# TODO: write the left hand chord
		beat += eighth_note

# write MIDI output
with open("logins.mid", "wb") as f:
	m.writeFile(f)