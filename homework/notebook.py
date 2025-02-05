#
# Descarga de datos
#
import pandas as pd


owner = "jdvelasq"
repo = "datalabs"
file = "datasets/demanda_comercial.csv"

file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{file}"


data = pd.read_csv(file_url, sep=";", decimal=",", thousands=".")
data.head()






#
# Se organizan los datos para graficarlos.
#
data_to_plot = data.copy()
data_to_plot = data_to_plot.melt(
    id_vars=["Fecha"], var_name="hora", value_name="demanda"
)
data_to_plot = data_to_plot.sort_values(by=["Fecha", "hora"])
data_to_plot = data_to_plot.reset_index(drop=True)
data_to_plot = data_to_plot.head(500)
data_to_plot.head()


# Crea una carpeta de salida
#
import os

if not os.path.exists("../files/plots"):
    os.makedirs("../files/plots")

if not os.path.exists("../files/data"):
    os.makedirs("../files/data")


    
    
    
import matplotlib.pyplot as plt
#
# Patrones de ejemplo
#
plt.figure(figsize=(7, 4))
plt.plot(data.loc["2017-06-05", :], ".-", color="tab:blue")
plt.plot(data.loc["2018-06-05", :], ".-", color="tab:orange")
plt.plot(data.loc["2022-06-03", :], ".-", color="tab:green")
plt.xticks(rotation=90)
plt.show()





#
# Se divide cada fila por el máximo de la fila para
# hacer adimensionales los datos
#
data = data.apply(lambda row: row / row.max(), axis=1)
data.head(10)










#
# Patrones de ejemplo
#
plt.figure(figsize=(7, 4))
plt.plot(data.loc["2017-06-05", :], ".-", color="tab:blue")
plt.plot(data.loc["2018-06-05", :], ".-", color="tab:orange")
plt.plot(data.loc["2022-06-03", :], ".-", color="tab:green")
plt.xticks(rotation=90)
plt.savefig("../files/plots/demanda-comercial-patrones-ejemplo.png")
plt.show()












#
# Determinación de la cantidad de perfiles diferentes
#
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

n_clusters = 10
scores = []

for n in range(2, n_clusters):

    kmeans = KMeans(n_clusters=n, n_init="auto")
    kmeans.fit(data)
    labels = kmeans.labels_
    scores.append(silhouette_score(data, labels, metric="euclidean"))


plt.figure(figsize=(5, 4))
plt.plot(range(2, n_clusters), scores, marker="o", color="tab:blue", alpha=0.9)
plt.xlabel("número de clusters")
plt.gca().spines["left"].set_color("gray")
plt.gca().spines["bottom"].set_color("gray")
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)
plt.grid()
plt.show()

















#
# Dos patrones óptimos
#
kmeans = KMeans(n_clusters=2, n_init="auto")
kmeans.fit(data)

plt.figure(figsize=(7, 4))
plt.plot(kmeans.cluster_centers_[0], ".-", color="tab:blue")
plt.plot(kmeans.cluster_centers_[1], ".-", color="tab:orange")
plt.savefig("../files/plots/demanda-comercial-perfiles.png")
plt.show()






#
# Adiciona el numero del cluster correspondiente a cada fila
# y agrega el día de la semana (como entero). El domingo
# es el día 0.
#
data = data.assign(cluster=kmeans.labels_)
data = data.assign(day=pd.to_datetime(data.index).day_of_week)
data[["cluster", "day"]]









#
# Calcula la frecuencia de cada día por cluster
#
data_per_cluster_0 = data.loc[data.cluster == 0, "day"]
days_cluster_0 = data_per_cluster_0.value_counts()
days_cluster_0 = days_cluster_0.sort_index()
days_cluster_0





data_per_cluster_1 = data.loc[data.cluster == 1, "day"]
days_cluster_1 = data_per_cluster_1.value_counts()
days_cluster_1 = days_cluster_1.sort_index()
days_cluster_1



































