import random

def fillBag(shape_list_index):
    shape_list_index.append(0)
    shape_list_index.append(1)
    shape_list_index.append(2)
    shape_list_index.append(3)
    shape_list_index.append(4)
    shape_list_index.append(5)
    shape_list_index.append(6)

def chooseFbag(shape_list_index):
    if not shape_list_index:
        fillBag(shape_list_index)

    choice = random.choice(shape_list_index)
    shape_list_index.remove(choice)
    return choice
