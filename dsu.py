# Disjoint set union/find functions used in Kruskal's algorithm

def dsuRoot(par, node):
	if par[node] == node:
		return node
	else:
		par[node] = dsuRoot(par, par[par[node]])
		return par[node]

def dsuMerge(par, node1, node2):
	par[dsuRoot(par, node2)] = dsuRoot(par, node1)