from typing import Dict, List
from .classifier_interface import ClassifierInterface
from src.datasets.dataset_interface import DatasetInterface
from math import inf
from heapq import nsmallest

class KnnClassifier(ClassifierInterface):
    def __init__(self) -> None:
        super().__init__()

    def train(self, train_dataset: DatasetInterface) -> None:
        # salvar as amostras do dataset
        train_samples = []
        for i in range(train_dataset.size()):
            train_samples.append(train_dataset.get(i))

        self.train_samples = train_samples

    def predict(self, test_dataset: DatasetInterface) -> List[str]:
        """ para cada amostra no dataset, buscar os k vizinhos mais proximos e 
        retornar a classe mais frequente entre eles """
        
        Ntests = test_dataset.size
        Nsamples = len(self.train_samples)
        K = 5

        test_samples = []
        for i in range(Ntests):
            test_samples.append(test_dataset.get(i))

        # Calcula as distancias euclidianas entre os objetos de teste e 
        # os objetos de treino, em seguida as salva em uma lista de listas
        distances = []
        distances_temp = []
        for i in range(Ntests):
            for j in range(Nsamples):
                sum = 0
                for k in range(len(test_samples[0][0])):
                    sum += (test_samples[i][0][k] - self.train_samples[j][0][k]) ** 2
                distances_temp.append(sum ** 0.5)
            distances.append(distances_temp)
            distances_temp = []

        # Cria uma lista de listas contendo os indices das 5 menores distancias
        smallest_k_dist_idx = []
        for i in range(Ntests):
            smallest_k_dist = nsmallest(K, distances[i])
            for j in range(K):
                smallest_k_dist[j] = distances[i].index(smallest_k_dist[j])
            smallest_k_dist_idx.append(smallest_k_dist)
            smallest_k_dist = []

        # Cria uma lista contendo as classes identificadas nos objetos de teste
        classes = []
        class_count = []
        predicted_classes = []
        for i in range(Ntests):
            for idx in smallest_k_dist_idx[i]:
                if not self.train_samples[idx][1] in classes:
                    classes.append(self.train_samples[idx][1])
                    class_count.append(1)
                else:
                    class_count[classes.index(self.train_samples[idx][1])] += 1
            predicted_classes.append(classes[class_count.index(max(class_count))])
            classes = []
            class_count = []

        # for i in range(len(predicted_classes)):
        #     print(f"{i}: {predicted_classes[i]}")

        return predicted_classes