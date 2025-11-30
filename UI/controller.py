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

        # 5. Recupero statistiche dal Model
        n_nodi = self._model.get_num_nodes()
        n_archi = self._model.get_num_edges()

        # Aggiungo le statistiche (Numero nodi e archi)
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di Hubs: {n_nodi}"))
        self._view.lista_visualizzazione.controls.append(ft.Text(f"Numero di Tratte: {n_archi}"))

        # 6. Recupero e Stampa degli Archi
        # get_all_edges restituisce una lista di tuple: (nodo_u, nodo_v, data_dict)
        all_edges = self._model.get_all_edges()

        for i, (u, v, data) in enumerate(all_edges, 1): #enumerate restituisce, a ogni passo del ciclo, una coppia (1 = start)
            weight = data.get('weight', 0)  # Come se dicessi: "Dammi il valore di 'weight'.
                                            # Se non lo trovi, dammi 0 come valore di default".

            # 'u' e 'v' sono INTERI OGGETTI di tipo Hub.
            # Per stamparli bene, accedo al loro codice o nome.
            nodo_start = str(u)
            nodo_end = str(v)

            row_txt = f"{i}) [{nodo_start} --> {nodo_end}] -- guadagno Medio Per Spedizione: {weight:.2f}€"

            self._view.lista_visualizzazione.controls.append(ft.Text(row_txt))

        # Messaggio se non ci sono archi
        if len(all_edges) == 0:
            self._view.lista_visualizzazione.controls.append(ft.Text("Nessuna tratta soddisfa i criteri di guadagno minimo."))

        # 7. Aggiornamento finale della pagina
        self._view.update()
        # TODO

