from pathlib import Path
import pymupdf


class LectorPDF:
    def __init__(self, ruta):
        self.ruta = Path(ruta)

    def leer(self):
        if not self.ruta.exists():
            raise FileNotFoundError(f'No existe: {self.ruta}')
        with pymupdf.open(self.ruta) as documento:
            return [
                {'pagina': n, 'texto': pagina.get_text()}
                for n, pagina in enumerate(documento, start=1)
            ]
