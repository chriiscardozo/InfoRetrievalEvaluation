import time
import sys
from util import tempo
from util import erro
import loader as Loader
import avaliador

def main():
	start = time.time()
	
	if(len(sys.argv) < 2):
		erro("\n\tUso: python3 main.py output_original [output_stem]")

	RP_AB = {}
	for path in sys.argv[1:]:
		print('\n\n\n******** AVALIANDO ' + path + ' ********\n\n')
		r_esperado, r_obtido = Loader.carregar_informacoes(path)
		relevancias = Loader.carregar_relevancias(path)		
		rp = avaliador.avaliar_resultados(r_esperado, r_obtido, path, relevancias)
		RP_AB[path] = rp

	if len(RP_AB) == 2:
		avaliador.construir_rp_ab(RP_AB)

	tempo(start, "executar_tudo")

if __name__ == '__main__':
	main()