import sqlite3
import os

#list of all functions

exit = False
command_list = {
	"help": "alias: '?', displays a list of commands",
	"quit": "alias: 'q', 'exit', hammertime",
	"addword": "alias: '+w', add a word to the lexicon",
	"addaddword": "alias: '++w', add a multitude words to the lexicon",
	"adddef": "alias: '+d', add a defination to the lexicon",
	"addadddef": "alias: '++d', add a multitude definations to the lexicon",
	"define": "alias: 'd', 'link', link a word with a definintion",
	"wordsearch": "alias: 'ws', search for a word",
	"defsearch": "alias: 'ds', search for a definition",
	"search": "alias: 's', search for a word and definition combo",
	"remove": "alias: 'r', removes a word, definition or link",
	"edit": "alias: 'e' edits a word, definition or link",
	"info": " made by osswix and bur, version 　六兰"
}
db = os.path.abspath("lex.db")
#link to the database location

#makes a connection with the database, and executes the given query
def _(*command):
	conn = sqlite3.connect(db)
	cur = conn.cursor()
	result = cur.execute(*command).fetchall()
	conn.commit()
	conn.close()
	return result


#dah beast itself!zzz
while not exit:
	command = input('fenhwi> ').lower()


	#print out the help menu
	if command == "help" or command == "?":
		# Print out the list of commands
		for entry in command_list:
			print("\t{0:10s}\t{1}".format(entry, command_list[entry]))


	#stops the program
	elif command == "quit" or command == "exit" or command == "q" or command == "hammertime":
		# Stops the program
		exit = True


	#adds a word
	elif command == "addword" or command == "+w":
		# Add a word
		hanji = None
		hangul = None
		roman = None
		hanji = input("Enter Hanji (if any): ")
		while not hangul:
			hangul = input("Enter The Hangul: ")
		while not roman:
			roman = input("Enter The Roman: ")
		_("INSERT INTO Words('Roman', 'hanja', 'Hangul') VALUES(?, ?, ?)", (roman, hanji, hangul))

	#adds a multitude words
	elif command == "addaddword" or command == "++w":
		# Add a word
		i = None
		while i == None :
			hanji = None
			hangul = None
			roman = None
			hanji = input("Enter Hanji (if any): ")
			if hanji == "quit" or hanji == "q" or hanji == "stop":
				i = "stop"
			else:
				while not hangul:
					hangul = input("Enter The Hangul: ")
				while not roman:
					roman = input("Enter The Roman: ")
				_("INSERT INTO Words('Roman', 'hanja', 'Hangul') VALUES(?, ?, ?)", (roman, hanji, hangul))
				print("word added")
		print("everything has been added")


	#searches for a word
	elif command == "wordsearch" or command == "ws":
		# Search for words
		search = input("Enter your search query: ")
		results = _("SELECT * FROM Words WHERE Roman LIKE ?", ("%{0}%".format(search),))
		print("\t{0:5s}\t{1:10s}\t{2:25s}\t{3}".format("UWID", "Hanji", "Hangul", "Roman"))
		for result in results:
			print("\t{0:5s}\t{1:10s}\t{2:25s}\t{3}".format(str(result[0]), result[2], result[3], result[1]))


	#adds a multitude definitions
	elif command == "addadddef" or command == "++d":
		# Add a definition
		i = None
		while i == None:
			definition = input("Enter your definition: ")
			if definition == "q" or definition == "quit" :
				i = "stop"
			else:
				_("INSERT INTO Definitions('Definition') Values(?)", (definition,))
				print("defenition added")
		print("everything has been added")



	#adds a definition
	elif command == "adddef" or command == "+d":
		# Add a definition
		definition = input("Enter your definition: ")
		_("INSERT INTO Definitions('Definition') Values(?)", (definition,))


	#searches for definitions
	elif command == "defsearch" or command == "ds":
		# Search for definitions
		search = input("Enter your search query: ")
		results = _("SELECT * FROM Definitions WHERE Definition LIKE ?", ("%{0}%".format(search),))
		print("\t{0:5s}\t\t{1}".format("UDID", "Definition"))
		for result in results:
			print("\t{0:5s}\t\t{1}".format(str(result[0]), result[1]))


	#links words with definitions
	elif command == "define" or command == "d" or command == "link":
		# Create a link
		uwid = input("Enter the word ID to define: ")
		udid = input("Enter the definition ID: ")
		_("INSERT INTO Link('F_UWID', 'F_UDID') Values(?, ?)", (uwid, udid))


	#initiates search
	elif command == "search" or command == "s":
		# Initiates a search query
		word_or_def = None

		#tests what to use for search
		while not word_or_def:
			i = input("Search by word [w] or definition [d]: ").lower()
			if i == "w" or i == "word":
				word_or_def = "word"
			elif i == "d" or i == "definition" or i == "def":
				word_or_def = "def"
			elif i == "back" or i == "b":
				word_or_def = "back"
			else:
				word_or_def = None

		#searches by word
		if word_or_def == "word":
			# Output Words that match roman query with definitions
			search = input("Enter your search query: ")
			results = _("SELECT * FROM Words WHERE Roman LIKE ?", ("%{0}%".format(search),))
			print("\t{0:25s}\t{1:10}\t{2}".format("Hangul","Hanji","roman"))
			for result in results:
				ids = [x[0] for x in _("SELECT F_UDID FROM Link WHERE F_UWID IS ?", (result[0],))]
				definitions = [_("SELECT Definition FROM Definitions WHERE UDID IS ?", (id,))[0][0] for id in ids]
				for definition in definitions:
					if definition == definitions[0]:
						print("\t{0:25s}\t{2:10s}\t{1}".format(result[3], definition, result[2]))
					else:
						print("\t{0:25s}\t{2:10s}\t{1}".format("", definition, ""))

		#searches by definition
		elif word_or_def == "def":
			# Output Words that match definition query with definitions
			search = input("Enter your search query: ")
			results = _("SELECT * FROM Definitions WHERE Definition LIKE ?", ("%{0}%".format(search),))
			print("\t{0:25s}\t{1:10s}\t{2}".format("Hangul","Hanji","Roman"))
			for result in results:
				ids = [x[0] for x in _("SELECT F_UWID FROM Link WHERE F_UDID IS ?", (result[0],))]
				words = [_("SELECT * FROM Words WHERE UWID IS ?", (id,))[0] for id in ids]
				for word in words:
					definition = _("SELECT Definition FROM Definitions WHERE UDID IS ?", (result[0],))[0][0]
					print("\t{0:25s}\t{1:10s}\t{2}".format(word[3], word[2], definition))

		#quits the search
		else:
			print("returning")


	#initiates deletion part
	elif command == "remove" or command == "r" or command == "delete" :
		word_def_or_link = None

		#tests what to
		while not word_def_or_link :
			i = input(" word [w] definition [d] or link [l]: ").lower()
			if i == "w" or i == "word":
				word_def_or_link = "word"
			elif i == "d" or i == "definition" or i == "def":
				word_def_or_link = "def"
			elif i == "l" or i == "link":
				word_def_or_link = "link"
			elif i == "b" or i == "back":
				word_def_or_link = "back"
			else :
				word_def_or_link = None

		#deleting a word
		if word_def_or_link == "word":
			delete = input("enter word ID to delete: ")
			blah = _("SELECT * FROM Link WHERE F_UWID IS ?", (delete,))
			if len(blah) == 0:
				_("DELETE FROM Words WHERE UWID IS ?", (delete,))
				print("word deleted")
			else:
				print("Please remove link")

		#deleting a definition
		elif word_def_or_link == "def":
			delete = input("enter definition ID to delete: ")
			blah = _("SELECT * FROM Link WHERE F_UDID IS ?", (delete,))
			if len(blah) == 0:
				_("DELETE FROM Definitions WHERE UDID IS ?", (delete,))
				print("definition deleted")
			else:
				print("please remove link")

		#deleting a link
		elif word_def_or_link == "link":
			delword = input("enter word id of link to delete: ")
			deldef = input("enter definition id of link to delte: ")
			_("DELETE FROM Link WHERE F_UWID IS ? AND F_UDID IS ?", (delword, deldef))
			print("link deleted")

		#abords deletion
		else:
			print("returning")


	#initiates the edit program
	elif command == "edit" or command == "e" :
		edit_what = None

		#tests what to edit
		while not edit_what :
			i = input("word [w] definition [d] or link [l]: ")
			if i == "w" or i == "word" :
				edit_what = "word"
			elif i == "d" or i == "definition" :
				edit_what = "def"
			elif i == "l" or i == "link" :
				edit_what = "link"
			elif i == "b" or i == "back" :
				edit_what = "back"
			else :
				edit_what = None

			#edit a word
		if edit_what == "word" :
			idq = input("enter word ID to edit: ")
			edit = None

			while not edit :
				inp = input("Hangul[h], hanji[j], or roman[r]: ")
				if inp == "hangul" or inp == "h" :
					edit = "han"
				elif inp == "hanji" or inp == "j" :
					edit = "ja"
				elif inp == "roman" or inp == "r" :
					edit = "rom"
				elif inp == "back" or inp == "b" :
					edit = "back"
				else :
					edit = None

			#either does nothing or asks for what to change to
			if edit == "back":
				print("returing")
			else :
				new = input("enter what to change the word to: ")

			#edits the word
			if edit == "han" :
				_("UPDATE Words SET Hangul = (?) WHERE UWID = (?)", (new, idq))
			elif edit == "ja" :
				_("UPDATE Words SET hanja = (?) WHERE UWID = (?)", (new, idq))
			elif edit == "rom" :
				_("UPDATE Words SET Roman = (?) WHERE UWID = (?)", (new, idq))
			else :
				print("")
			idq = None
			print("updated")

		#edit a definition
		elif edit_what == "def" :
			i = input("enter definition ID to edit: ")
			e = input("enter what to change the definition to: ")
			_("UPDATE Definitions SET Definition = (?) WHERE UDID = (?)", (e, i))
			print("updated")
		#edit a link
		elif edit_what =="link" :
			oldword = input("enter the old word id: ")
			olddef = input("enter the old definition id: ")
			newword = input("enter the new word id: ")
			newdef = input("enter the new definition id: ")
			_("UPDATE Link SET F_UWID = (?), F_UDID = (?) WHERE F_UWID = (?) AND F_UDID = (?)", (newword, newdef, oldword, olddef))
			print("updated")
		else :
			print("returning")


	#shows the command is unknown error
	else:
		print("Command: '{0}' is not recognised".format(command))



#project initiated by Bur_Sanjun(something) (Sam Blumire)
#project finished by Osswix (Wilco Jacobs)
#project used by Osswix (Wilco Jacobs)
#versions beforehand do not have any form of update
#version 　六兰
#note that the version is day of the month + month in fenhwi itself.
#changelog from 一兰 to 六兰
#replaced hanja with hanji (spelling correction)
#added ways to quickly add multiple words.
