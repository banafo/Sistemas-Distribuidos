# Servidor de echo usando RPC 
import rpyc #modulo que oferece suporte a abstracao de RPC

#servidor que dispara um processo filho a cada conexao
from rpyc.utils.server import ForkingServer,ThreadedServer 
from collections import deque
from collections import defaultdict,deque
from threading import Thread, Lock
from random import randint

# porta de escuta do servidor de echo
PORTA = 10039
lock = Lock()
#graph1 = {}
di = {}
node_id = {}

f = open("graph1.txt", "w")

'''graph1 = {
	0: [1, 2], 
	1: [2], 
	2: [0, 3], 
	3: [3]
}
'''
#funçao de eleição auxiliar 
def exposed_dfs(graph,node):
	print("Graph: ",di)
	visited = []
	stack = deque()
	fin = []

	visited.append(node)
	stack.append(node)
	while stack:
		s = stack.pop()
		fin.append(s)
		print(s, end=' ')
		for n in reversed(graph[s]):
			if n not in visited:
				visited.append(n)
				stack.append(n)
	return fin


# classe que implementa o servico de echo
class Echo(rpyc.Service):
	# executa quando uma conexao eh criada
	def on_connect(self, conn):
		print("Conexao iniciada:")

	# executa quando uma conexao eh fechada
	def on_disconnect(self, conn):
		print("Conexao finalizada:")

	# função para fazer eleição
	def exposed_election(self, msg):
		print("nodes ids: ", node_id)
		lista = []
		#ler arquivo de Grafo
		with open("graph1.txt", "r") as fi:
			for line in fi:
				parts = line.split()
				#print (parts)
				for i in range(1,len(parts)):
					#print(i)
					lista.append(int(parts[i]))
					#print(lista)
				di[int(parts[0])] = lista   #criar dicionario aparte do arquvo
				lista = []
		ret = exposed_dfs(di, msg)
		if len(ret) > 1: 
			check = ret[1:]
			maior_id  = check[0]
			for i in check:
				if node_id[i] > maior_id:
					maior_id = node_id[i]
					results = ['sequencia '+str(ret),'node '+str(i) ,'id '+str(maior_id)] #retorna a sequencia do grafo,o nó com maior id
		else:
			results = ['sequencia '+str(ret),'node '+str(ret[0]) ,'id '+str(node_id[ret[0]])]

		print(di)
		return results

	# faz registro de todos os nós que connecta com servidor
	def exposed_register(self, node, neighbour):
		#lock.acquire()
		node_id[node] = randint(5,100)

		#criar arquivo de grafo
		g = open("graph1.txt", "a+")
		g.write(str(node))
		for i in neighbour:
			g.write(' '+str(i))
		g.write('\n')
		print("Neighbours Registered")
		#lock.release()
 

		#return fin
  
# dispara o servidor
if __name__ == "__main__":

	srv = ThreadedServer(Echo, port=PORTA)
	srv.start()
	#srv = ForkingServer(Echo, port = PORTA)
	#srv.start()