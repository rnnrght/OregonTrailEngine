class Parser:
	def __init__(self):
		data = open("Game.dat", "r")
		self.gameParams = {}
		for line in data:
			if line.strip() == "":	 #skipping blank lines like this
				continue #lets us keep the data file more readable

			attribute = line.split(":")
			try:
				self.gameParams[attribute[0].strip()] = attribute[1].strip()
			except IndexError:
				self.gameParams[attribute[0].strip()] = ""

	def allAttributes(self):
		return self.gameParams
	
	def get(self, paramName):
		try:
			return self.gameParams[paramName]
		except KeyError:
			return ""

if __name__ == '__main__' : #run this file directly for a quick self-test
	parser = Parser()
	print parser.allAttributes()
