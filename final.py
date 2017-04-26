from scanner import Scanner 
import sys
import re

class my_table:
	def __init__(self, file):
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
	
	def cart_prod(self, x, y):
		T1 = self.tables[x-1]
		T2 = self.tables[y-1]
		product = my_table("prod")	
		for i in range(0, T1.rows):
			for j in range(0, T2.rows):
				new_row = T1.table[j] + T2.table[j]
				product.table.append(new_row)
		product.rows = T1.rows * T2.rows
		product.cols = T1.cols + T2.cols
		product.meta = T1.meta + T2.meta
		return product		

def display_table(T1):
	print(T1.meta)
	for i in range(0, T1.rows):
		for j in range(0, T1.cols):
			sys.stdout.write(T1.table[i][j] + "\t")
		print(" ")
def main():
	T1 = my_table("T1.txt")
	T1.create_table()
	T2 = my_table("T2.txt")
	T2.create_table()
	T3 = my_table("T3.txt")
	T3.create_table()
	data = db(T1, T2, T3)
	T4 = data.cart_prod(1, 2)
	#display_table(T1)
	#display_table(T2)
	#display_table(T3)
	#display_table(T4)
main()
