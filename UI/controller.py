import flet as ft
from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def mostra_tratte(self, e):
        """
        Funzione che controlla prima se il valore del costo inserito sia valido (es. non deve essere una stringa) e poi
        popola "self._view.lista_visualizzazione" con le seguenti info
        * Numero di Hub presenti
        * Numero di Tratte
        * Lista di Tratte che superano il costo indicato come soglia
        """
        # 1. Recupero input dalla View
        input_str = self._view.guadagno_medio_minimo.value

        # 2. Validazione
        try:
            if input_str == "":
                raise ValueError  # Gestisco stringa vuota come errore
            threshold = float(input_str)
        except ValueError:
            self._view.show_alert("Errore: Inserire un valore numerico valido per il guadagno medio!")
            self._view.update()
            return

        # 3. Costruzione Grafo tramite Model
        # Questo metodo resetta il grafo e lo ricrea con i filtri
        self._model.costruisci_grafo(threshold)

        # 4. Aggiornamento UI
        self._view.lista_visualizzazione.controls.clear()

        # Recupero statistiche dal Model
        n_nodi = self._model.get_num_nodes()
        n_archi = self._model.get_num_edges()


        # TODO

