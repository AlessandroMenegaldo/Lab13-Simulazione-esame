import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    def fillDD(self):
        years = self._model.getAllYears()
        for a in years:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._view.update_page()

    def fillDDShape(self, e):
        year = self._view.ddyear.value
        if year is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona prima un Anno"))
            return
        print(year)

        shapes = self._model.getShapes(year)
        for s in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(s))

        self._view.update_page()


    def handle_graph(self, e):
        year = self._view.ddyear.value
        shape = self._view.ddshape.value

        if year is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona prima un Anno"))
            return
        if shape is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Seleziona prima una forma"))
            return

        listaPesi = self._model.buildGraph(year, shape)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato --> Nodi: {self._model.getNumNodi()}  Archi: {self._model.getNumArchi()}"))
        self._view.txt_result.controls.append(ft.Text("Elenco nodi:"))
        for n in listaPesi:
            self._view.txt_result.controls.append(ft.Text(f"{n[0]}  ({n[1]})"))

        self._view.update_page()

    def handle_path(self, e):
        self._model.getBestPath()