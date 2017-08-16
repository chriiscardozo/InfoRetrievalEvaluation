import ast
import csv
import os

FILE_ESPERADO="output_pc_esperados.csv"
FILE_RESULTADO="output_busca.csv"

def carregar_informacoes(src_dir):
	esperados = {}
	with open(os.path.join(src_dir, FILE_ESPERADO), 'r') as f:
		reader = csv.reader(f, delimiter=';')
		next(reader)
		for row in reader:
			qry_number = row[0]
			doc_number = row[1]
			if(qry_number not in esperados): esperados[qry_number] = [doc_number]
			else: esperados[qry_number].append(doc_number)

	obtidos = {}
	with open(os.path.join(src_dir, FILE_RESULTADO), 'r') as f:
		reader = csv.reader(f, delimiter=';')
		for row in reader:
			qry_number = row[0]
			tmp = ast.literal_eval(row[1])
			if(tmp[2] > 0.001): # zero threshold
				if(qry_number not in obtidos): obtidos[qry_number] = [tmp[1]]
				else: obtidos[qry_number].append(str(tmp[1]))

	return (esperados,obtidos)

def carregar_relevancias(src_dir):
	relevancias = {}
	with open(os.path.join(src_dir, FILE_ESPERADO), 'r') as f:
		reader = csv.reader(f, delimiter=';')
		next(reader)
		for row in reader:
			qry_number = row[0]
			doc_number = row[1]
			if(qry_number not in relevancias):
				relevancias[qry_number] = {}
			relevancias[qry_number][doc_number] = int(row[2])
	return relevancias