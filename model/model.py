import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self.G = nx.DiGraph()
        self.artists = []

    def get_roles(self):
        return DAO.read_role()

    def get_artists(self, role):
        return DAO.read_connections(role)

    def names(self):
        return DAO.read_names()

    def build_graph(self, role: str):
        id_connessioni = DAO.read_connections(role)
        for el in id_connessioni:
            self.artists.append(el)
        self.G.add_nodes_from(self.artists)
        edges = []
        for art1 in id_connessioni:
            for art2 in id_connessioni:
                if art1 != art2 and id_connessioni[art1].p != id_connessioni[art2].p:
                    if id_connessioni[art1].p>id_connessioni[art2].p and (art1, art2,id_connessioni[art1].p-id_connessioni[art2].p ) not in edges:
                        edges.append((art1, art2,id_connessioni[art1].p-id_connessioni[art2].p ))
                    elif id_connessioni[art2].p>id_connessioni[art1].p and (art2, art1,id_connessioni[art2].p-id_connessioni[art1].p ) not in edges:
                        edges.append((art2, art1,id_connessioni[art2].p-id_connessioni[art1].p ))
        self.G.add_weighted_edges_from(edges)
        return len(self.artists), len(edges)

    def classifica(self):
        classifica = {}
        for el in self.artists:
            classifica[el] = self.G.out_degree(el) - self.G.in_degree(el)
        print(classifica)
        print(list(classifica))
        return classifica

    def cerca_percorso(self, source, lunghezza_esatta):
        print(self.G.nodes)
        self.best_path = []
        self.max_weight = -float("inf")

        def dfs(nodo_corrente, path_parziale, peso_parziale):
            archi_attuali = len(path_parziale) - 1

            if archi_attuali == lunghezza_esatta:

                if peso_parziale > self.max_weight:
                    self.max_weight = peso_parziale
                    self.best_path = list(path_parziale)
                return

            for vicino in self.G.neighbors(nodo_corrente):
                if vicino not in path_parziale:
                    peso_arco = self.G[nodo_corrente][vicino]['weight']

                    path_parziale.append(vicino)

                    dfs(vicino, path_parziale, peso_parziale + peso_arco)

                    path_parziale.pop()

        dfs(source, [source], 0)
        return self.best_path, self.max_weight
