from typing import Tuple, Any, Dict
from .dataset_interface import DatasetInterface
from .stop_words import Stop_words

class NewsDataset(DatasetInterface):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        # ler arquivo contendo os nomes dos arquivos de noticias e as classes
        self.path = path
        self.newsPath = []
        self.newsClass = []
        with open(path) as file:
            for line in file:
                self.newsPath.append(line[:-5])
                self.newsClass.append(line[-4:-1])

    def size(self) -> int:
        # retornar o numero de noticias no dataset (numero de linhas no arquivo)
        self.size = len(self.newsPath)
        return self.size

    def get(self, idx: int) -> Tuple[Any, str]:
        # ler a i-esima noticia do disco e retornar o texto como uma string e a classe
        newPath = self.path[:self.path.rfind("/") + 1] + self.newsPath[idx]
        with open(newPath) as file:
            text = file.readlines()[0].split()

        for word in text[:]:
            if word in Stop_words.stop_words:
                text.remove(word)
        
        return text, self.newsClass[idx]