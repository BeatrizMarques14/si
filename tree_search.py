# Module: tree_search
# 
# This module provides a set o classes for automated
# problem solving through tree search:
#    SearchDomain  - problem domains
#    SearchProblem - concrete problems to be solved
#    SearchNode    - search tree nodes
#    SearchTree    - search tree with the necessary methods for searhing
#
#  (c) Luis Seabra Lopes
#  Introducao a Inteligencia Artificial, 2012-2019,
#  Inteligência Artificial, 2014-2019

from abc import ABC, abstractmethod

# Dominios de pesquisa
# Permitem calcular
# as accoes possiveis em cada estado, etc
class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    def actions(self, state):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal
    def goal_test(self, state):
        return self.domain.satisfies(state,self.goal)

# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self,state,parent,cost): 
        self.state = state
        self.parent = parent
        self.cost = cost
        self._length = None
        
    @property
    def length(self):
        if self._length is None:
            if self.parent is None:
                self._length = 0
            else:
                self._length = self.parent.length + 1
        return self._length
    	
    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + "," + str(self.depth) + "," + str(self.length) + ")"
    def __repr__(self):
        return str(self)

# Arvores de pesquisa
class SearchTree:

    # construtor
    def __init__(self,problem, strategy='breadth',depth_limit=None): 
        self.problem = problem
        root = SearchNode(problem.initial, None,0)
        self.open_nodes = [root]
        self.strategy = strategy
        self.solution = None
        self.explored_states = set()  # Conjunto para armazenar estados explorados
        self.depth_limit = depth_limit

        
    @property
    def length(self):
        if self.solution is None:
            return 0
        return self.solution.length


    # obter o caminho (sequencia de estados) da raiz ate um no
    def get_path(self,node):
        if node.parent == None:
            return [node.state]
        path = self.get_path(node.parent)
        path += [node.state]
        return(path)

    # procurar a solucao
    def search(self, limit=None):
        self.non_terminals = 0
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
           
            	
            if self.problem.goal_test(node.state):
                self.solution = node
                self.terminals = len(self.open_nodes) + 1
                return self.get_path(node)
            
            self.non_terminals+=1
               
            
            self.explored_states.add(node.state)
            
            if limit== None or node.depth<limit:
                lnewnodes = []
                for a in self.problem.domain.actions(node.state):
                    newstate = self.problem.domain.result(node.state,a)
                
                    if newstate not in self.explored_states:
                        cost = node.cost + self.problem.domain.cost(node.state,a)
                        newnode = SearchNode(newstate,node,cost)
                        lnewnodes.append(newnode)
            
            self.add_to_open(lnewnodes)

                
        return None
        

        
   

    # juntar novos nos a lista de nos abertos de acordo com a estrategia
    def add_to_open(self,lnewnodes):
        if self.strategy == 'breadth':
            self.open_nodes.extend(lnewnodes)
        elif self.strategy == 'depth':
            self.open_nodes[:0] = lnewnodes
        elif self.strategy == 'uniform':
            pass
            
    @property
    def avg_branching(self):
    	return(self.terminals + self.non_terminals - 1)

