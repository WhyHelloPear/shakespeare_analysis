import csv
import operator

class Play:
	def __init__(self, name):
		self.name = name #tracks name of play
		self.words = [] #tracks unique word count for a play
		self.character_lines = {} #tracks characters and how many lines they have in a play
		self.character_words = {} #tracks characters and how many words they have in a play


	def character_line(self, character):
		if character in self.character_lines:
			self.character_lines[character] += 1
		else:
			self.character_lines[character] = 1

	def character_word(self, character, amount):
		if character in self.character_words:
			self.character_words[character] += amount
		else:
			self.character_words[character] = amount

	def unique_words(self, words):
		for word in words:
			if word not in self.words:
				self.words.append(word)


def get_play(plays, name):
	for play in plays:
		if play.name == name:
			return play


def main():

	plays = []

	with open('Shakespeare_data.csv', newline='') as csvfile:
		file = csv.reader(csvfile, delimiter=',')
		i = 0
		last_char = ""
		last_line = ""
		for row in file:
			if i != 0:

				if (row[5] == "ACT I") or ("SCENE I" in row[5]): #new play
					play = get_play(plays, row[1])
					if play == None:
						play = Play(row[1])
						plays.append(play)
				if row[3] != '': #line delivered by character

					if(row[2] != last_line) and (row[4] != last_char):
						play.character_line(row[4])

					play = get_play(plays, row[1])

					line = row[5]
					line = line.replace(",", '')
					line = line.replace('.', '')
					line = line.replace('?', '')
					line = line.replace('!', '')
					line = line.replace(';', '')
					line = line.replace(':', '')

					words = line.split(" ")

					play.character_word(row[4], len(words))
					play.unique_words(words)

					last_line = row[2]
					last_char = row[4]

			i += 1

	with open("./results.csv", "w") as csv_file:
		writer = csv.writer(csv_file, delimiter=',')

		for play in plays:
			string = '\n' + play.name + '\n'
			string += '# of Unique Words: ' + str(len(play.words)) + '\n\n'
			
			char_lines = sorted(play.character_lines.items(), key=operator.itemgetter(1), reverse=True)

			for i in range(5):
				char = char_lines[i][0]
				string += char + "......#lines:" + str(play.character_lines[char]) + "......#words:" + str(play.character_words[char]) + '\n'
			
			string += '\n-------------------------------------------------------\n'
			writer.writerow([string])


main()