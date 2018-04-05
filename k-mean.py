from functools import reduce
import random
import math

WINDOW_HEIGHT = 600;
WINDOW_WIDTH = 600;

points_count = 1000;
classes_count = 8;

def initialize_points():
    points = [{
        'x': random.randint(0, WINDOW_WIDTH),
        'y': random.randint(0, WINDOW_HEIGHT),
        'class': 0,
    } for point in range(points_count)]
    return points

def initialize_centroids(points):
    centroids = [points[i] for i in random.sample(range(points_count), classes_count)]
    for i in range(classes_count):
        centroids[i].update({"class": i})
    return centroids

def euclid_distance(a, b):
    return math.sqrt((a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2)


def allocate_classes(points, centroids):
    for i in range(points_count):
        centroid = min(centroids, key=lambda x: euclid_distance(points[i], x))
        points[i].update({"class": centroid["class"]})

def find_new_centroids(points):
    new_centroids = []
    for i in range(classes_count):
        class_points = list(filter(lambda x: x["class"] == i, points))
        sum_centroid = reduce((lambda prev, current: {"x": prev["x"] + current["x"], "y": prev["y"] + current["y"]}), class_points)
        new_centroids.append({"class": i, "x": round(sum_centroid["x"] / len(class_points)), "y": round(sum_centroid["y"] / len(class_points)),})
    return new_centroids

def equal_centroids(a, b):
    for i in range(classes_count):
        if (a[i]["x"] != b[i]["x"] or a[i]["y"] != b[i]["y"] or a[i]["class"] != b[i]["class"]):
            return False
    return True

def main():
    points = initialize_points()
    centroids = initialize_centroids(points)
    continue_clasterization = True
    while (continue_clasterization):
        allocate_classes(points, centroids)
        new_centroids = find_new_centroids(points)
        equal = equal_centroids(new_centroids, centroids)
        centroids = new_centroids
        if (equal):
            continue_clasterization = False

if __name__ == "__main__":
    main()
