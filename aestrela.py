import pygame #modulo de graficos 2D 
import math
from queue import PriorityQueue 

LARGURA = 700 # tamanho da janela 
JAN = pygame.display.set_mode((LARGURA, LARGURA)) #configurando o display usando a mesma dimensão pra linhas e colunas
pygame.display.set_caption("Algoritmo de busca A*") #adiciono um titulo para a janela


#adicionado alguns codigos para utilizar cores mais tarde
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 255, 0)
AMARELO = (255, 255, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165 ,0)
CINZA = (128, 128, 128)
TURQUESA = (64, 224, 208)

class Node: #cada nó do nosso grafo vai ser um quadrado do nosso plano 2D
	def __init__(self, lin, col, largura, total_lins):
		self.lin = lin #linha
		self.col = col #coluna
		self.x = lin * largura #coordenada x da posição
		self.y = col * largura #coordenada y da posição
		self.color = BRANCO #estado inicial indicado por branco, ou seja vazio
		self.neighbors = [] #lista de vizinhos
		self.largura = largura #tamanho
		self.total_lins = total_lins #numero total de linhas

	def get_pos(self): #retorna a posição
		return self.lin, self.col

	def is_closed(self): #metodo para indicar que o node já foi avaliado
		return self.color == VERMELHO

	def is_open(self): #indicar que o node está na fila para ser avaliado (conjunto open)
		return self.color == VERDE

	def is_barrier(self): #indica se é um obstaculo/parede do labirinto
		return self.color == PRETO

	def is_inicio(self): #indicar o ponto de partida
		return self.color == LARANJA

	def is_fim(self): #indicar o destino
		return self.color == TURQUESA

	def reset(self): #restaura o estado inicial
		self.color = BRANCO

	def make_inicio(self):
		self.color = LARANJA

	def make_closed(self):
		self.color = VERMELHO

	def make_open(self):
		self.color = VERDE
#em seguida metodos para mudar o estado do node
	def make_barrier(self):
		self.color = PRETO

	def make_fim(self):
		self.color = TURQUESA

	def make_path(self):
		self.color = ROXO

	def draw(self, win): #metodo para desenhar o node no display
		pygame.draw.rect(win, self.color, (self.x, self.y, self.largura, self.largura))

	def update_neighbors(self, grid): #metodo para atualizar a lista de vizinhos
		self.neighbors = [] #devem ser adicioado os nodes vizinhos que não sejam paredes
		if self.lin < self.total_lins - 1 and not grid[self.lin + 1][self.col].is_barrier(): #node abaixo
			self.neighbors.append(grid[self.lin + 1][self.col])

		if self.lin > 0 and not grid[self.lin - 1][self.col].is_barrier(): #node acima
			self.neighbors.append(grid[self.lin - 1][self.col])

		if self.col < self.total_lins - 1 and not grid[self.lin][self.col + 1].is_barrier(): #node a direita
			self.neighbors.append(grid[self.lin][self.col + 1])

		if self.col > 0 and not grid[self.lin][self.col - 1].is_barrier(): #node a esquerda
			self.neighbors.append(grid[self.lin][self.col - 1])

	def __lt__(self, other): #diferencia o node dos outros
		return False

#função heuristica para calcular a distancia de dois nodes 
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2) #retorna a soma de nodes que precisamos caminhar em x e y do ponto p1 para o p2


def reconstruct_path(veio_de, atual, draw): #reconstroi o caminho realizado pra chegar ao node destino
	while atual in veio_de:
		atual = veio_de[atual] #encadeia em serie 
		atual.make_path() #muda o estado do node, pra indicar que faz parte do caminho encontrado
		draw() #atualiza a visualização da aplicação


def algorithm(draw, grid, inicio, fim):
	count = 0 #usar a ordem(quem cntrou primeiro) como criterio de desempate em caso de valores iguais para f
	open_set = PriorityQueue()
	open_set.put((0, count, inicio)) #adicionar para a fila de prioridade o ponto inicial com f_score = 0
	veio_de = {} #guardar de qual node o node atual era vizinho, para podermos traçarmos o caminho
	g_score = {node: float("inf") for lin in grid for node in lin} #valor inicial para os nodes não observados
	g_score[inicio] = 0 #valor inicial do node inicial (distancia dele até ele mesmo)
	f_score = {node: float("inf") for lin in grid for node in lin} #valor inicial para os nodes não observados
	f_score[inicio] = h(inicio.get_pos(), fim.get_pos()) #calcula a distancia do inicio ao fim

	open_set_hash = {inicio} #indicar quais os nodes estão no conjunto open(para serem avaliados)

	while not open_set.empty(): #até não sobrar nenhum item na lista
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit() #encerra se aplicação for fechada
		
		#inicio da avaliação do node
		atual = open_set.get()[2] #pegamos o node de melhor valor
		open_set_hash.remove(atual) #e indicamos que o node foi removido do conjunto open

		if atual == fim: #se chegamos no destino
			#traçar o caminho do fim pro inicio, oridentado pela sequencia de qual node veio
			# de qual node, até que encontremos o node inicial
			reconstruct_path(veio_de, fim, draw) 
			fim.make_fim()
			return True

		for neighbor in atual.neighbors: #para todos os vizinhos do node avaliado
			temp_g_score = g_score[atual] + 1 #contamos um passo dado em relação ao ponto inicial

			#se chegamos nesse node com menos passos que antes, nós atualizamos os valores g, f e o caminho
			if temp_g_score < g_score[neighbor]: 
				veio_de[neighbor] = atual
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), fim.get_pos())
				if neighbor not in open_set_hash: #se o vizinho não estiver na lista para ser avaliado
					count += 1 #numera a ordem
					open_set.put((f_score[neighbor], count, neighbor)) #coloca ele na lista
					open_set_hash.add(neighbor)
					neighbor.make_open()#indica que esta no conjunto open na aplicação (colore o node)

		draw()#atualiza visualmente a aplicação (re desenha os elementos com os novos valores)

		if atual != inicio: #não mudaremos a cor do node inicial
			atual.make_closed() #após o node ser avaliado, sinalizamos que está no "conjunto closed"

	return False #se chegou nessa linha ainda não achamos o caminho até o destino, continuamos o laço

#criar uma estrutura para permitir a manipulação dos pontos
def make_grid(lins, largura):
	grid = []
	gap = largura // lins #comprimento de cada nó
	for i in range(lins):
		grid.append([])
		for j in range(lins):
			node = Node(i, j, gap, lins)
			grid[i].append(node)

	return grid

#função para desenhar linhas separando os nós, para ficar mais facil de ver
def draw_grid(win, lins, largura):
	gap = largura // lins
	for i in range(lins):
		pygame.draw.line(win, CINZA, (0, i * gap), (largura, i * gap))
		for j in range(lins):
			pygame.draw.line(win, CINZA, (j * gap, 0), (j * gap, largura))

#desenhar os nodes e as linhas no display
def draw(win, grid, lins, largura):
	win.fill(BRANCO)

	for lin in grid:
		for node in lin:
			node.draw(win)

	draw_grid(win, lins, largura)
	pygame.display.update()

#retornar a posição do node que foi clicado pelo mouse
def get_clicked_pos(pos, lins, largura):
	gap = largura // lins
	y, x = pos

	lin = y // gap #o numero da linha e da coluna é a posição do mouse divido pelo tamanho do node
	col = x // gap

	return lin, col


def main(win, largura):
	LINS = 50 #quantidade de linhas e colunas (onde cada elemento é um node)
	grid = make_grid(LINS, largura) #instanciar o grid

	inicio = None #variavel para indicar a entrada/começo do labirinto
	fim = None #variavel para indicar a saida/fim

	run = True
	while run:
		draw(win, grid, LINS, largura) #mostra os nodes e as linhas (e atualiza)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:#parar aplicação quando fechado
				run = False

			if pygame.mouse.get_pressed()[0]: #click esquerdo
				pos = pygame.mouse.get_pos()
				lin, col = get_clicked_pos(pos, LINS, largura)
				node = grid[lin][col]
				if not inicio and node != fim:#se inicio não está definido, define
					inicio = node
					inicio.make_inicio()

				elif not fim and node != inicio:#se o fim nao está definido, define
					fim = node
					fim.make_fim()

				elif node != fim and node != inicio:#então faz uma parede/obstaculos
					node.make_barrier()

			elif pygame.mouse.get_pressed()[2]: #click direito, "limpar"
				pos = pygame.mouse.get_pos()
				lin, col = get_clicked_pos(pos, LINS, largura)
				node = grid[lin][col]
				node.reset() # desfaz uma atribuição feita a algum node, volta para o estado branco
				if node == inicio:
					inicio = None
				elif node == fim:
					fim = None

			if event.type == pygame.KEYDOWN: 
				if event.key == pygame.K_SPACE and inicio and fim: #se espaço for pressionado
					for lin in grid:
						for node in lin:
							node.update_neighbors(grid) #atualiza os vizinhos, excluindo os obstaculos/paredes
					#iniciar o algoritmo de busca, e mostrar a busca e o resultado
					algorithm(lambda: draw(win, grid, LINS, largura), grid, inicio, fim)

				if event.key == pygame.K_r: #se pressionado r
					inicio = None #reseta a aplicação 
					fim = None
					grid = make_grid(LINS, largura)

	pygame.quit() #encerra a aplicação

main(JAN, LARGURA) #inicia a aplicação