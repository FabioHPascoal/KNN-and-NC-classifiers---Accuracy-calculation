from typing import Tuple, Any, Dict
from .dataset_interface import DatasetInterface
import cv2

class ImageDataset(DatasetInterface):
    def __init__(self, path: str) -> None:
        super().__init__(path)
        # ler arquivo contendo os nomes das imagens e as classes e armazenar
        # em uma lista
        self.path = path
        self.imagePath = []
        self.imageClass = []
        with open(path) as file:
            for line in file:
                self.imagePath.append(line[:-3])
                self.imageClass.append(line[-2:-1])

    def size(self) -> int:
        # retornar tamanho do dataset (numero de linhas do arquivo)
        self.size = len(self.imagePath)
        return self.size

    def get(self, idx: int) -> Tuple[Any, str]:
        # ler a i-esima imagem do disco usando a biblioteca cv2 e retornar
        # a imagem vetorizada e sua respectiva classe
        newPath = self.path[:self.path.rfind("/") + 1] + self.imagePath[idx]
        image = cv2.imread(newPath, 0)
        
        flattened_image = []
        for i in range(len(image)):
            for j in range(len(image[0])):
                flattened_image.append(int(image[i][j]))
        
        return flattened_image, self.imageClass[idx]