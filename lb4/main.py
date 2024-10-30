import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# Загрузка данных
DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "WineDataset.csv"))
df = pd.read_csv(DATA_PATH)

# Проверка данных и вычисление статистики
print(df.describe())

# Визуализация статистики
df.hist(bins=50, figsize=(20, 15))
plt.show()

# Обработка отсутствующих значений
df = df.dropna()

# Масштабирование данных (нормализация)
features = df.columns[:-1]  # Все столбцы, кроме Wine

# Вычисляем среднее и стандартное отклонение для каждого признака
means = df[features].mean()
stds = df[features].std()

# Нормализируем значения
df[features] = (df[features] - means) / stds

# Разделение на обучающий и тестовый наборы
X = df[features].values
y = df["Wine"].values
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# Функция для вычисления расстояния между двумя точками
def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))


# Реализация k-NN
def k_nearest_neighbors(X_train, y_train, X_test, k):
    predictions = []
    for X_test_instance in X_test:
        distances = []
        for i, train_instance in enumerate(X_train):
            distance = euclidean_distance(X_test_instance, train_instance)
            distances.append((distance, y_train[i]))

        # Сортировка по расстоянию и выбор k ближайших
        distances.sort(key=lambda x: x[0])
        neighbors = distances[:k]

        # Получение метки по большинству голосов
        classes = [neighbor[1] for neighbor in neighbors]
        majority_vote = max(set(classes), key=classes.count)
        predictions.append(majority_vote)
    return predictions


# Оценка модели на тестовом наборе
def evaluate_knn(X_train, y_train, X_test, y_test, k):
    y_pred = k_nearest_neighbors(X_train, y_train, X_test, k)
    accuracy = np.mean(y_pred == y_test)
    return accuracy, y_pred


# Функция для случайного выбора признаков
def select_random_features(X_train, X_test, num_features):
    feature_indices = np.random.choice(X_train.shape[1], num_features, replace=False)
    return X_train[:, feature_indices], X_test[:, feature_indices]


# Модель 1: Случайные признаки
num_random_features = 3  # Число случайных признаков
X_train_1, X_test_1 = select_random_features(X_train, X_test, num_random_features)

# Модель 2: Фиксированный набор признаков (Алкоголь, Магнезиум, Интенсивность цвета)
X_train_2 = X_train[:, [0, 3, 9]]
X_test_2 = X_test[:, [0, 3, 9]]


def confusion_matrix(y_true, y_pred):
    unique_labels = np.unique(y_true)
    matrix = np.zeros((len(unique_labels), len(unique_labels)), dtype=int)
    for true, pred in zip(y_true, y_pred):
        matrix[int(true) - 1, int(pred) - 1] += 1
    return matrix


def plot_confusion_matrix(y_true, y_pred, model_num, k):
    conf_matrix = confusion_matrix(y_true, y_pred)
    print(f"Confusion Matrix для модели {model_num} (k={k}):")
    print(conf_matrix)


# Оценка модели 1 и визуализация матрицы ошибок для разных значений k
for k in [3, 5, 10]:
    accuracy_1, y_pred_1 = evaluate_knn(X_train_1, y_train, X_test_1, y_test, k)
    print(f"Точность для модели 1 (случайные признаки) при k={k}: {accuracy_1}")
    plot_confusion_matrix(y_test, y_pred_1, model_num=1, k=k)

# Оценка модели 2 и визуализация матрицы ошибок для разных значений k
for k in [3, 5, 10]:
    accuracy_2, y_pred_2 = evaluate_knn(X_train_2, y_train, X_test_2, y_test, k)
    print(f"Точность для модели 2 (фиксированные признаки) при k={k}: {accuracy_2}")
    plot_confusion_matrix(y_test, y_pred_2, model_num=2, k=k)


# 3D-визуализация нескольких признаков
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection="3d")
ax.scatter(df["Alcohol"], df["Magnesium"], df["Color intensity"], c=df["Wine"])
ax.set_xlabel("Alcohol")
ax.set_ylabel("Magnesium")
ax.set_zlabel("Color intensity")
plt.show()
