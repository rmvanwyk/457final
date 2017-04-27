from scanner import Scanner 
import sys
import re

class my_table:
	def __init__(self, file = None, name = None):
		self.name = name
		self.filename = file
		self.rows = 0
		self.cols = 0
		self.col_name = ""
		self.table = []
		self.meta = [] 

	def create_table(self):
		scan = Scanner(self.filename) 
		meta = scan.readline()
		meta = meta.rstrip()
		self.meta = meta.split("\t")
		self.cols = len(self.meta)
		self.rows = 0
		input = scan.readline()
		while (input != ""):
			row = input.rstrip()
			row = row.split("\t")
			self.table.append(row)
			input = scan.readline() 
			self.rows += 1
		 
class db:
	def __init__(self, T1, T2, T3):
		self.tables = [T1, T2, T3]
	
	def cart_prod(self, T1, T2, lvl):
		product = my_table("prod", 4)	
		for i in range(0, T1.rows):
			for j in range(0, T2.rows): 
				if int(T1.table[i][T1.cols-1]) <= lvl and int(T2.table[j][T2.cols-1]) <= lvl and int(T1.table[i][1]) == int(T2.table[j][1]):
					TC = max(int(T1.table[i][T1.cols-1]), int(T2.table[j][T2.cols-1]))
                                        new_row = T1.table[i][0:T1.cols-1] + T2.table[j]
					new_row[len(new_row)-1] = str(TC)                    #possible source of error???
                                        product.table.append(new_row)
                                        product.rows += 1
		product.meta = T1.meta[0:T1.cols-1] + T2.meta
		product.cols = T1.cols-1 + T2.cols
		return product		

def display_table(T1):
	print(T1.meta)
	for i in range(0, T1.rows):
		for j in range(0, T1.cols):
			sys.stdout.write(T1.table[i][j] + "\t")
		print(" ")
class query:
	def __init__(self):
		self.level = 0
		self.selectc = []
		self.fromc = []
		self.wherec = []

	def prompt(self):
		scan = Scanner("")
		sys.stdout.write("Level: ")
		level = scan.readint()
		sys.stdout.write("SELECT: ")
		selectc = scan.readline()	
		sys.stdout.write("FROM: ")
		fromc = scan.readline()	
		sys.stdout.write("WHERE: ")
		wherec = scan.readline()
		wherec = wherec.strip()
    		wherec = wherec.split("and")
		wheref = []
		i = 0
		while (i < len(wherec)):
			wherec[i] = wherec[i].strip()
			wheref.append(wherec[i].split("="))
			i += 1
		wheref2 = wheref[len(wheref)-1][1].replace(";","")
		wheref[len(wheref)-1][1] = wheref2
		fromc = fromc.strip()
		fromc = fromc.split(", ")	
		selectc = selectc.strip()
		selectc = selectc.split(", ")
		self.level = level
		self.selectc = selectc
		self.fromc = fromc
		self.wherec = wheref	
	
	def process(self, data):
		TempTable = my_table()
      		#FullTable = my_table()
		for i in range(0, len(data.tables)):
			if self.fromc[0] == data.tables[i].name:
				TempTable = data.tables[i]
				break	
		if len(self.fromc) > 1:
			for i in range(1, (len(self.fromc))):
                		for j in range(0, len(data.tables)):
					if self.fromc[i] == data.tables[j].name:
						TempTable = data.cart_prod(TempTable, data.tables[j], self.level)
		#FullTable.meta = TempTable.meta
		#FullTable.cols = TempTable.cols
		for i in range(0, (len(self.wherec))):
          		InterTable = my_table()
			InterTable.meta = TempTable.meta
			InterTable.cols = TempTable.cols
          		for j in range(0, (len(self.wherec[i])-1)):
            			cond1 = self.wherec[i][j]
            			cond2 = self.wherec[i][j+1]
            			c1index = TempTable.meta.index(cond1)
            			if cond2.isdigit():
              				for k in range(0, TempTable.rows):
              					if int(TempTable.table[k][c1index]) == int(cond2) and int(TempTable.table[k][TempTable.cols-1]) <= self.level: 
							row = TempTable.table[k]
              						InterTable.table.append(row)
							InterTable.rows += 1	
            			else:
              				c2index = TempTable.meta.index(cond2)
              				for k in range(0, TempTable.rows):
              					if int(TempTable.table[k][c1index]) == int(TempTable.table[k][c2index]) and int(TempTable.table[k][TempTable.cols-1]) <= self.level: 
							row = TempTable.table[k]
              						InterTable.table.append(row)
							InterTable.rows += 1	
				TempTable = InterTable             
				j+=1
			#FullTable = TempTable
		return TempTable	
			
def main():
	T1 = my_table("T1.txt","T1")
	T1.create_table()
	T2 = my_table("T2.txt","T2")
	T2.create_table()
	T3 = my_table("T3.txt","T3")
	T3.create_table()
	data = db(T1, T2, T3)
	Q = query()
	Q.prompt()
	T4 = my_table()
	T4 = Q.process(data) 
	display_table(T4)
main()
