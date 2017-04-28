from scanner import Scanner 
import sys
import re

class my_table:
	def __init__(self, file = None, name = None):
		self.name = name
		self.filename = file
		self.rows = 0
		self.cols = 0
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

class query:
	def __init__(self):
		self.level = 0
		self.selectc = []
		self.fromc = []
		self.wherec = []

	def prompt(self):
		scan = Scanner("")
		sys.stdout.write("Level ")
		level = scan.readint()
		sys.stdout.write("SELECT ")
		selectc = scan.readline()	
		sys.stdout.write("FROM ")
		fromc = scan.readline()	
		sys.stdout.write("WHERE ")
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
		temp_T = my_table()
		for i in range(0, len(data.tables)):
			if self.fromc[0] == data.tables[i].name:
				temp_T = data.tables[i]
				break	
		if len(self.fromc) > 1:
			for i in range(1, (len(self.fromc))):
                		for j in range(0, len(data.tables)):
					if self.fromc[i] == data.tables[j].name:
						temp_T = data.cart_prod(temp_T, data.tables[j], self.level)
		for i in range(0, (len(self.wherec))):
          		inter_T = my_table()
			inter_T.meta = temp_T.meta
			inter_T.cols = temp_T.cols
          		for j in range(0, (len(self.wherec[i])-1)):
            			c_1 = self.wherec[i][j]
            			c_2 = self.wherec[i][j+1]
				if c_1 == "TC" and int(c_2) > self.level:
					raise ValueError('Error: Security Level Violation.')
					sys.exit()	
            			c1_ind = temp_T.meta.index(c_1)
            			if c_2.isdigit():
              				for k in range(0, temp_T.rows):
              					if int(temp_T.table[k][c1_ind]) == int(c_2) and int(temp_T.table[k][temp_T.cols-1]) <= self.level: 
							row = temp_T.table[k]
              						inter_T.table.append(row)
							inter_T.rows += 1	
            			else:
              				c2_ind = temp_T.meta.index(c_2)
              				for k in range(0, temp_T.rows):
              					if int(temp_T.table[k][c1_ind]) == int(temp_T.table[k][c2_ind]) and int(temp_T.table[k][temp_T.cols-1]) <= self.level: 
							row = temp_T.table[k]
              						inter_T.table.append(row)
							inter_T.rows += 1	
				temp_T = inter_T             
				j+=1
		return temp_T	
			
	def select_cols(self,T1):
		if self.selectc[0]=='*':
			if T1.cols > 6:
				KCi = 1
				for i in range(1, T1.cols):
					if T1.meta[i] == "KC":
						T1.meta[i] = "KC" + str(KCi)
						KCi += 1
			return T1
		else:
			T2 = my_table()
			col_nums = []
			for i in range(0, len(self.selectc)):
				cond = self.selectc[i]
				col_ind = T1.meta.index(cond)
				if col_ind not in col_nums:
					col_nums.append(col_ind)
					T2.cols += 1
				if T1.meta[col_ind] == "A1" or T1.meta[col_ind] == "B1" or T1.meta[col_ind] == "C1":
					col_nums.append(T1.meta.index(cond)+1)
					T2.cols += 1
			if (T1.cols-1) not in col_nums:
				col_nums.append(T1.cols-1)
				T2.cols += 1
			row = []
			KCi = 1
			for i in range(0, len(col_nums)):
				if str(T1.meta[col_nums[i]]) == "KC":
					T2.meta.append("KC" + str(KCi))
					KCi += 1
				else:
					T2.meta.append(T1.meta[col_nums[i]])
			for i in range(0, T1.rows):
				for j in range(0, len(col_nums)):
					row.append(T1.table[i][col_nums[j]])
				T2.table.append(row)
				T2.rows += 1
				row = []
			return T2	

class db:
	def __init__(self, T1, T2, T3):
		self.tables = [T1, T2, T3]
	
	def cart_prod(self, T1, T2, lvl):
		prod = my_table("prod", 4)	
		for i in range(0, T1.rows):
			for j in range(0, T2.rows): 
				if int(T1.table[i][T1.cols-1]) <= lvl and int(T2.table[j][T2.cols-1]) <= lvl and int(T1.table[i][1]) == int(T2.table[j][1]):
					TC = max(int(T1.table[i][T1.cols-1]), int(T2.table[j][T2.cols-1]))
                                        new_row = T1.table[i][0:T1.cols-1] + T2.table[j]
					new_row[len(new_row)-1] = str(TC)
                                        prod.table.append(new_row)
                                        prod.rows += 1
		prod.meta = T1.meta[0:T1.cols-1] + T2.meta
		prod.cols = T1.cols-1 + T2.cols
		return prod		

def display_table(T):
	print("RESULTS: " )
	for i in range(0, len(T.meta)):
		sys.stdout.write(T.meta[i] + "\t")
	print("")
	for i in range(0, 7*T.cols):
		sys.stdout.write("=")
	print("")
	for i in range(0, T.rows):
		for j in range(0, T.cols):
			sys.stdout.write(T.table[i][j] + "\t")
		print(" ")

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
	results = my_table()
	results = Q.process(data) 
	results = Q.select_cols(results) 
	display_table(results)
main()
