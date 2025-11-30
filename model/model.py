from database.dao import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._nodes = None
        self._edges = None
        self.G = nx.Graph()
        # Mappe per accesso rapido (id -> oggetto)
        self._id_map = {}

    def costruisci_grafo(self, threshold):
        """
        Costruisce il grafo (self.G) inserendo tutti gli Hub (i nodi) presenti e filtrando le Tratte con
        guadagno medio per spedizione >= threshold (euro)
        """
        # 1. Pulizia: Se il grafo esiste già, lo svuoto
        self.G.clear()
        self._nodes = set()
        self._edges = set()

        # 2. Recupero tutti gli Hub dal DB
        all_hubs = DAO.get_hub()

        # 3. Aggiungo i nodi al grafo
        for hub in all_hubs:
            # Salvo nella mappa per recuperare l'oggetto dato l'ID
            self._id_map[hub.id] = hub
            self._nodes.add(hub)

            # Aggiungo il nodo al grafo (passo l'intero oggetto)
            self.G.add_node(hub)

        # 4. Recupero tutte le tratte (archi potenziali)
        all_tratte = DAO.get_tratta()  # Metodo corretto nel turno precedente

        # 5. Aggiungo gli archi filtrando
        for tratta in all_tratte:
            # Calcolo guadagno medio: richiamo metodo della classe tratta
            if tratta.n_spedizioni > 0:
                peso = tratta.peso_tratta()
            else:
                peso = 0

        # FILTRO: Aggiungo l'arco solo se la media supera la soglia
            if peso > float(threshold):
                # Recupero gli oggetti nodo reali usando la mappa
                u = self._id_map[tratta.h1]
                v = self._id_map[tratta.h2]

                # Aggiungo l'arco
                self.G.add_edge(u, v, weight=peso)

        return self.G

        # TODO

    def get_num_edges(self):
        """
        Restituisce il numero di Tratte (edges) del grafo
        :return: numero di edges del grafo
        """
        return self.G.number_of_edges()
        # TODO

    def get_num_nodes(self):
        """
        Restituisce il numero di Hub (nodi) del grafo
        :return: numero di nodi del grafo
        """
        return self.G.number_of_nodes()
        # TODO

    def get_all_edges(self):
        """
        Restituisce tutte le Tratte (gli edges) con i corrispondenti pesi
        :return: gli edges del grafo con gli attributi (il weight)
        """
        return self.G.edges(data=True) # Restituisce una lista di tuple (nodo1, nodo2, dizionario_attributi)
        # TODO

