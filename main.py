import time
import sys
from util import tempo
from util import erro
import loader as Loader
import avaliador

def main():
	start = time.time()
	
	if(len(sys.argv) != 2):
		erro("\n\tUso: python3 main.py work_dir")

	r_esperado, r_obtido = Loader.carregar_informacoes(sys.argv[1])
	relevancias = Loader.carregar_relevancias(sys.argv[1])

	avaliador.avaliar_resultados(r_esperado, r_obtido, sys.argv[1], relevancias)

	tempo(start, "executar_tudo")

if __name__ == '__main__':
	main()