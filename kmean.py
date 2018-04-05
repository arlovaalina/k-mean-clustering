from functools import reduce
from tkinter import *
from variables import *
import random
import math

def paint_points(points, centroids):
    canvas.delete("all")
    for i in range(0, points_count):
        canvas.create_oval(points[i]["x"], points[i]["y"], points[i]["x"] + 1, points[i]["y"] + 1,
            fill=COLORS[points[i]["class"]], outline=COLORS[points[i]["class"]])
    for j in range(0, classes_count):
        canvas.create_oval(centroids[j]["x"], centroids[j]["y"], centroids[j]["x"] + 10, centroids[j]["y"] + 10,
            fill=COLORS[centroids[j]["class"]], outline=COLORS[centroids[j]["class"]])

def initialize_points():
    points = [{
        'x': random.randint(0, FIELD_WIDTH),
        'y': random.randint(0, FIELD_HEIGHT),
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

def start_algorithm(event):
    print('start')
    points = initialize_points()
    centroids = initialize_centroids(points)
    continue_clasterization = True
    while (continue_clasterization):
        paint_points(points, centroids)
        root.update()
        allocate_classes(points, centroids)
        new_centroids = find_new_centroids(points)
        equal = equal_centroids(new_centroids, centroids)
        centroids = new_centroids
        if (equal):
            continue_clasterization = False
    print('finish')


root = Tk()
root.geometry("{0}x{1}".format(WINDOW_WIDTH, WINDOW_HEIGHT))
canvas = Canvas(root, width = FIELD_WIDTH, height = FIELD_HEIGHT, borderwidth = 1, background='white')
canvas.place(x = 200, y = 10)
start_button = Button(root, text = "Start algorithm", width = 10)
start_button.place(x = 20, y = 10)
start_button.bind("<Button-1>", start_algorithm)

root.mainloop()
