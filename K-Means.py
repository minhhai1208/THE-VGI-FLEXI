import numpy as np
import matplotlib.pyplot as plt


def generate_clusters(n_points=50, shift=(0, 0)):
    return 1.0*np.random.randn(n_points, 2) + shift

def custom_kmeans(data, k, maxit=10):
    random_number = np.random.choice(data.shape[0], k, replace=False)
    centroid = data[random_number]
    centroids_his = [centroid]
    labels_his =[]
    
    for _ in range(maxit):
        distances = np.linalg.norm(data[:,np.newaxis]-centroid, axis=2)
        
        labels = np.argmin(distances, axis=1)
        
        new_centroid = np.array([data[labels==k].mean(axis=0) for k in range(k)])
        print(new_centroid)

        # Check for convergence
        if np.all(centroid == new_centroid):
            break
        centroids = new_centroid
        centroids_his.append(centroids)
        labels_his.append(labels)
    return centroids_his, labels_his
    
    # Function to plot clusters and centroids
def plot_clusters(data, centroids, ax, step, labels=None):
    if labels is not None:
        ax.scatter(data[labels == 0][:, 0], data[labels == 0][:, 1],
        color='blue', s=50, alpha=0.6)
        ax.scatter(data[labels == 1][:, 0], data[labels == 1][:, 1],
        color='red', s=50, alpha=0.6)
        ax.scatter(data[labels == 2][:, 0], data[labels == 2][:, 1],
        color='green', s=50, alpha=0.6)
    else:
        ax.scatter(data[:, 0], data[:, 1], color='grey', s=50, alpha=0.6)
        ax.scatter(centroids[:, 0], centroids[:, 1], color='black', marker='x',
              s=100)
        ax.set_title("Step: " + str(step))




cluster_1 = generate_clusters(shift=(5, 5))
cluster_2 = generate_clusters(shift=(-5, -5))
cluster_3 = generate_clusters(shift=(-0, -0))

# Combine the clusters
data = np.vstack([cluster_1, cluster_2, cluster_3])
# Apply custom k-means clustering
centroids_history, labels_history = custom_kmeans(data, k=3)
# Plot each step
fig, axes = plt.subplots(nrows=1, ncols=len(centroids_history),
figsize=(5*len(centroids_history), 5))
step=1
for ax, centroids, labels in zip(axes, centroids_history, [None] +
labels_history):
    plot_clusters(data, centroids, ax, step, labels)
    step+=1
#plt.tight_layout()
plt.show()