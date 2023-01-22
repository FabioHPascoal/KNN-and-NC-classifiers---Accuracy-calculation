from typing import Dict, List
from .classifier_interface import ClassifierInterface
from src.datasets.dataset_interface import DatasetInterface
from src.datasets.news_dataset import NewsDataset
from operator import add
import numpy as np

class NearestCentroidClassifier(ClassifierInterface):
    def __init__(self) -> None:
        super().__init__()

    def train(self, train_dataset: DatasetInterface) -> None:
        """ calcular os centroides por classe """

        # Guardando os dados de treino em uma lista
        train_samples = []
        Nsamples = train_dataset.size()
        for i in range(Nsamples):
            train_samples.append(train_dataset.get(i))
       
        # Vetorizacao dos textos do grupo de treino
        if isinstance(train_dataset, NewsDataset):         
            all_words = []
            for i in range(Nsamples):
                for word in train_samples[i][0]:
                    if not word in all_words:
                        all_words.append(word)

            for i in range(Nsamples):
                word_count = [0] * len(all_words)
                for word in train_samples[i][0]:
                    if word in all_words:
                        word_count[all_words.index(word)] += 1
                train_samples[i] = (word_count, train_samples[i][1])

            self.all_words = all_words
        
        # Calculo dos centroides
        classes = []
        class_sum = []
        class_count = []
        for i in range(Nsamples):
            Class = train_samples[i][1]
            Vector = train_samples[i][0]
            if not Class in classes:
                classes.append(Class)
                class_sum.append(Vector)
                class_count.append(1)
            else:
                class_sum[classes.index(Class)] = list(map(add, class_sum[classes.index(Class)], Vector))
                class_count[classes.index(Class)] += 1

        centroids = []
        for i in range(len(classes)):
            centroids.append(([item / class_count[i] for item in class_sum[i]], classes[i]))

        self.centroids = centroids
        self.class_sum = class_sum

    def predict(self, test_dataset: DatasetInterface) -> List[str]:
        """ para cada amostra no dataset, buscar o centroide mais proximo e respectiva retornar a classe """
        
        Ntests = test_dataset.size
        Ncentroids = len(self.centroids)

        # Guardando os dados de teste em uma lista
        test_samples = []
        for i in range(Ntests):
            test_samples.append(test_dataset.get(i))

        # Vetorizacao dos textos do grupo de teste
        if isinstance(test_dataset, NewsDataset):
            for i in range(Ntests):
                word_count = [0] * len(self.all_words)
                for word in test_samples[i][0]:
                    if word in self.all_words:
                        word_count[self.all_words.index(word)] += 1
                test_samples[i] = (word_count, test_samples[i][1])

        # Calcula as distancias euclidianas entre os objetos de teste e 
        # cada centroide, em seguida as salva em uma lista de listas
        distances = []
        distances_temp = []
        for i in range(Ntests):
            for j in range(Ncentroids):
                sum = 0
                for k in range(len(test_samples[0][0])):
                    sum += (test_samples[i][0][k] - self.centroids[j][0][k]) ** 2
                distances_temp.append(sum ** 0.5)
            distances.append(distances_temp)
            distances_temp = []

        # Cria uma lista contendo as classes identificadas nos objetos de teste
        predicted_classes = []
        for i in range(Ntests):
            smallest_dist = min(distances[i])
            predicted_classes.append(self.centroids[distances[i].index(smallest_dist)][1])

        # # Printa o numero de ocorrencias das palavras mais comuns de cada classe
        # for i in range(len(self.centroids)):
        #     print(self.centroids[i][1])
        #     most_occurrences_idx = np.argsort(self.class_sum[i])[-20:]
        #     for idx in most_occurrences_idx:
        #         print(f'{self.all_words[idx]} = {self.class_sum[i][idx]}')
        #     print("")

        return predicted_classes