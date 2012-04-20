import time
import nogil

def timer(func):
	def wrapper(*arg):
		t1 = time.time()
		func(*arg)
		t2 = time.time()
		print "%s took %0.3f ms" % (func.func_name, (t2-t1)*1000.0)
	return wrapper

@timer
def loopone():
	count = 5000000
	while count != 0:
		count -= 1

@timer
def looptwo():
	count = 5000000
	nogil.nogil(1,count)

@timer
def loopthree():
	count = 5000000
	nogil.nogil(2,count)

@timer
def loopfour():
	count = 5000000
	nogil.nogil(4,count)
	
@timer
def loopfive():
	count = 5000000
	nogil.nogil(6,count)
		
def main():
	loopone()
	looptwo()
	loopthree()
	loopfour()
	loopfive()
	
if __name__ == '__main__':
	main()
