import time

def tempo(start, task, minutes=False):
	den = 1.0
	units = " segundos"
	if(minutes):
		den = 60.0
		units = " minutos\t"

	print("T =",round((time.time()-start)/den), units, " (", task, ")")

def erro(msg, exiting=True):
	print("[Erro]", msg)
	if(exiting): exit(0)