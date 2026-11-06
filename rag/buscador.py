import numpy as np
from sentence_transformers import SentenceTransformer


class BuscadorRAG:
    def __init__(self, paginas):
        self.fragmentos = []
        for pagina in paginas:
            # Fragmentos con solapamiento para no perder contexto entre cortes.
            texto = ' '.join(pagina['texto'].split())
            for inicio in range(0, len(texto), 700):
                parte = texto[inicio:inicio + 900]
                if len(parte) > 40:
                    self.fragmentos.append({'pagina': pagina['pagina'], 'texto': parte})
                if inicio + 900 >= len(texto):
                    break
        if not self.fragmentos:
            raise ValueError('El PDF no contiene texto recuperable')
        self.modelo = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.vectores = self.modelo.encode(
            [f['texto'] for f in self.fragmentos], normalize_embeddings=True
        )

    def buscar(self, pregunta, top_k=3):
        vector = self.modelo.encode([pregunta], normalize_embeddings=True)[0]
        similitudes = self.vectores @ vector
        indices = np.argsort(similitudes)[::-1][:top_k]
        return [dict(self.fragmentos[int(i)], similitud=float(similitudes[i])) for i in indices]
