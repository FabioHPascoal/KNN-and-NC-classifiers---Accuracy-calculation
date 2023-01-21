from typing import Dict, List
from .classifier_interface import ClassifierInterface
from src.datasets.dataset_interface import DatasetInterface
from operator import add

class NearestCentroidClassifier(ClassifierInterface):
    def __init__(self) -> None:
        super().__init__()

    def train(self, train_dataset: DatasetInterface) -> None:
        """ calcular os centroides por classe """
        classes = []
        class_sum = []
        class_count = []
        for i in range(train_dataset.size()):
            Class = train_dataset.get(i)[1]
            Vector = train_dataset.get(i)[0]
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

    def predict(self, test_dataset: DatasetInterface) -> List[str]:
        """ para cada amostra no dataset, buscar o centroide mais proximo e respectiva retornar a classe """
        
        Ntests = test_dataset.size
        Ncentroids = len(self.centroids)

        test_samples = []
        for i in range(Ntests):
            test_samples.append(test_dataset.get(i))

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

        # for i in range(len(predicted_classes)):
        #     print(f"{i}: {predicted_classes[i]}")

        return predicted_classes