import matplotlib
import matplotlib.pyplot as plt
import os
import math

def recall(set_esperado,set_obtido):
	tp = len(set(set_esperado).intersection(set_obtido))
	return tp/len(set_esperado)

def precision(set_esperado,set_obtido):
	tp = len(set(set_esperado).intersection(set_obtido))
	return tp/len(set_obtido)

def calcular_precision_medio(esperado, obtido):
	sum_pr = 0
	for qry in esperado: sum_pr += precision(esperado[qry], obtido[qry])
	return sum_pr/float(len(esperado))

def calcular_recall_medio(esperado, obtido):
	sum_rec = 0
	for qry in esperado: sum_rec += recall(esperado[qry], obtido[qry])
	return sum_rec/float(len(esperado))

def calcular_f1(esperado, obtido, beta=1):
	print("\nCalculando medida F1")
	avg_precision = calcular_precision_medio(esperado,obtido)
	avg_recall = calcular_recall_medio(esperado, obtido)
	print('Precision avg:', avg_precision)
	print('Recall avg:', avg_recall)
	F1 = (((beta*beta) + 1) * avg_precision * avg_recall)/((beta*beta*avg_precision) + avg_recall)
	print('F1 value:', F1)

def get_precision_para_recall(esperado_qry,obtido_qry,min_recall):
	if(min_recall == 0): return 0

	for i in range(len(obtido_qry))[1:]:
		subset = obtido_qry[0:i]		
		if(min_recall <= recall(esperado_qry, subset)*100):
			return precision(esperado_qry, subset)
	return precision(esperado_qry, obtido_qry)

def interpolar_pontos_direita(points):
	size = len(points)
	i = size-1
	while i > 0:
		if points[i] > points[i-1]: points[i-1] = points[i]
		i -= 1
	return points

def calcular_grafico_11pontos(esperado,obtido,path):
	print("\nCalculando grafico de 11 pontos RxP (percent)")

	qry_points = {}
	cont = 0
	for k in esperado:
		qry_points[k] = []
		for i in range(11):
			valor_recall = i * 10
			valor_precision = get_precision_para_recall(esperado[k], obtido[k], valor_recall)
			qry_points[k].append(valor_precision)

		qry_points[k] = interpolar_pontos_direita(qry_points[k])
		#if(cont%10==0): print('Query', cont, 'de', len(esperado))
		cont += 1

	final_points = []
	for i in range(11):
		avg = 0
		for k in esperado: avg += qry_points[k][i]
		final_points.append(avg/len(esperado)*100)
	print('11-points:',str(final_points))
	plt.clf()
	plt.plot([x*10 for x in range(11)],final_points, 'b.-')
	plt.xlabel('recall')
	plt.ylabel('precision')

	for a,b in zip([x*10 for x in range(11)],final_points):
		plt.text(a,b,str(round(b, 3)))

	plt.savefig(os.path.join(path,'11points.png'))

def calcular_map(esperado,obtido):
	print('\nCalculando medida MAP')
	qry_avgs = []

	for qry_number in esperado:
		precision_sum = 0.0
		changes = 0

		recall_atual = 0.0
		for i in range(len(obtido[qry_number]))[1:]:
			subset = obtido[qry_number][0:i]
			novo_recall = recall(esperado[qry_number], subset)
			if(novo_recall != recall_atual):
				precision_sum += precision(esperado[qry_number], subset)
				changes += 1
				recall_atual = novo_recall
		qry_avgs.append(precision_sum/changes)

	print('MAP score:', sum(qry_avgs)/len(esperado))

def calcular_p5_p10(esperado, obtido):
	print('\nCalculando P@5 e P@10')
	p5 = 0
	p10 = 0
	for qry_number in esperado:
		p5 += precision(esperado[qry_number], obtido[qry_number][:5])
		p10 += precision(esperado[qry_number], obtido[qry_number][:10])
	print("Avg P@5:", p5/len(esperado))
	print("Avg P@10:", p10/len(esperado))

def calcular_MRR(esperado, obtido):
	print('\nCalculando MRR')
	mrr_sum = 0.0
	for qry_number in esperado:
		for i, item in enumerate(obtido[qry_number]):
			if item in esperado[qry_number]:
				mrr_sum += (1/(i+1))
				break

	print("MRR avg score:", mrr_sum/len(esperado))

def calcular_NDCG(esperado, obtido, relevancias):
	print('\nCalculando NDCG')
	soma_final = 0.0
	for qry_number in esperado:
		soma = 0.0
		ideal = []
		for i, doc in enumerate(obtido[qry_number]):
			rel = relevancias[qry_number][doc] if doc in relevancias[qry_number] else 0
			ideal.append(rel)
			soma += (rel/math.log(i+2,2)) # i+2 because i starts at zero
		
		ideal = sorted(ideal,reverse=True)
		soma_ideal = 0.0
		
		for i, rel in enumerate(ideal):
			soma_ideal += (rel/math.log(i+2, 2)) # i+2 because i starts at zero

		soma_final += (soma/soma_ideal)
	print("NDCG score:", soma_final/len(esperado))

def calcular_bpref(esperado, obtido):
	print('\nCalculando BPREF')
	soma_final = 0.0
	for qry_number in esperado:
		qtd_irrelevantes = 0
		soma = 0.0
		for doc in obtido[qry_number]:
			if(doc not in esperado[qry_number]):
				qtd_irrelevantes += 1
				if(qtd_irrelevantes == len(esperado[qry_number])):
					break
			else:
				soma += (1 - (qtd_irrelevantes/len(esperado[qry_number])))

		soma_final += 1/len(esperado[qry_number])*soma

	print('BPREF avg score:', soma_final/len(esperado))

def calcular_vetor_rp(esperado, obtido):
	print('\nCalculando vetor RP-A')
	rp = []
	for qry_number in esperado:
		rp.append(precision(esperado[qry_number], obtido[qry_number][:len(esperado[qry_number])]))

	print('R-Precision avg:', sum(rp)/len(esperado))
	return rp

def avaliar_resultados(esperado, obtido, path, relevancias):
	calcular_f1(esperado, obtido)
	calcular_grafico_11pontos(esperado,obtido,path)
	calcular_map(esperado, obtido)
	calcular_p5_p10(esperado, obtido)
	calcular_MRR(esperado, obtido)
	calcular_NDCG(esperado, obtido, relevancias)
	calcular_bpref(esperado, obtido)

	return calcular_vetor_rp(esperado, obtido)

def construir_rp_ab(dic):
	print('\nCalculando histograma RP-A/B')
	keys = list(dic.keys())
	wins_a = 0
	wins_b = 0
	empate = 0
	rp_ab = []
	for i, item in enumerate(dic[keys[0]]):
		v = item - dic[keys[1]][i]
		rp_ab.append(v)
		if(v > 0.0001): wins_a += 1
		elif(v < -0.0001): wins_b += 1
		else: empate += 1

	print("WINS_"+keys[0]+" =", wins_a, "/ WINS_"+keys[1]+" =", wins_b, "/ EMPATE =", empate)
	plt.clf()
	plt.xlabel('Query number')
	plt.ylabel('R-Precision A/B')
	plt.bar([x for x in range(len(dic[keys[0]]))], rp_ab)
	plt.savefig(os.path.join('rp_ab.png'))