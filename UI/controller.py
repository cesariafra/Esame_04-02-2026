import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def popola_dd_ruolo(self):
        self._view.popola_dropdown_ruolo(self._model.get_roles())

    def handle_crea_grafo(self, e):
        self._model.get_artists(self._view.dd_ruolo.value)
        n, e = self._model.build_graph(self._view.dd_ruolo.value)
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Nodi: {n} | Archi {e}"))
        self._view.btn_classifica.disabled = False
        self._view._page.update()

    def handle_classifica(self, e):
        nomi = self._model.names()
        classifica = self._model.classifica()
        self._view.list_risultato.controls.clear()
        self._view.list_risultato.controls.append(ft.Text(f"Artisti per influenza"))

        for el in classifica:
            self._view.list_risultato.controls.append(ft.Text(f"{nomi[el]} --> Delta = {classifica[el]}"))

        self._view.btn_cerca_percorso.disabled = False
        self._view.dd_iniziale.disabled = False
        self._view.input_L.disabled = False
        self.fill_dropdown()
        self._view._page.update()

    def fill_dropdown(self):
        self._view.dd_iniziale.options.clear()
        nomi = self._model.names()
        artists = self._model.artists
        for el in artists:
            option = ft.dropdown.Option(text=nomi[el], key=el)
            self._view.dd_iniziale.options.append(option)

        self._view.dd_iniziale.update()

    def handle_cerca_percorso(self, e):
        nomi = self._model.names()

        try:
            val = int(self._view.input_L.value)
        except ValueError:
            self._view.show_alert("Inserire valore ammissibile")
            return
        artists = self._model.artists

        if val < 3 or  val > len(artists):
            self._view.show_alert("Inserire valore ammissibile")
            return

        path, p = self._model.cerca_percorso(int(self._view.dd_iniziale.value), int(self._view.input_L.value))
        self._view.list_risultato.controls.clear()

        for el in path:
            self._view.list_risultato.controls.append(ft.Text(f"{nomi[el]} -->"))
        self._view.list_risultato.controls.append(ft.Text(f"(peso totale = {p})"))

        self._view._page.update()
