import random
# List of Tetrominoes: T J L I O S Z

def fillBag(shape_list_index):
    shape_list_index.append(0)
    shape_list_index.append(1)
    shape_list_index.append(2)
    shape_list_index.append(3)
    shape_list_index.append(4)
    shape_list_index.append(5)
    shape_list_index.append(6)

def chooseFbag(shape_list_index, shape_first):
    if not shape_list_index:
        fillBag(shape_list_index)

    if shape_first == True:
        shape_first = False
        shape_list_index = [0, 1, 2, 3, 4]
        shape_index = random.choice(shape_list_index)
        shape_list_index.remove(shape_index)
        return shape_index
    
    else:
        shape_index = random.choice(shape_list_index)
        shape_list_index.remove(shape_index)
        return shape_index
        