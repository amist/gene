import sys
import pickle
import matplotlib.pyplot as plt

def display_tree():
    generations_data = pickle.load(open('generations_data.p', 'rb'))
    cur_individuals = set([generations_data[-1][0]])
    print([x for x in cur_individuals])
    for i in range(len(generations_data)-2, -1, -1):
        cur_parents = set([x[0] for x in cur_individuals] + [x[1] for x in cur_individuals] + [x[2] for x in cur_individuals])
        #print(sorted(cur_parents))
        print(len(cur_parents))
        cur_individuals = set([x for x in set(generations_data[i]) if x[0] in cur_parents])
        
        
def show_individual(id):
    generations_data = pickle.load(open('generations_data.p', 'rb'))
    for generation in generations_data:
        for individual in generation:
            if individual[0] == id:
                print(individual)
                return
                
                
def create_graph(individuals_number):
    generations_data = pickle.load(open('generations_data.p', 'rb'))
    xs = [x for x in range(len(generations_data))]
    ys = [[-generation[i][3] for generation in generations_data] for i in range(individuals_number)]
    colors = ['r', 'b', 'g', 'c', 'y', 'm', 'k', 'r', 'b', 'g', 'c', 'y', 'm', 'k', 'r', 'b', 'g', 'c', 'y', 'm', 'k', 'r', 'b', 'g', 'c', 'y', 'm', 'k']
    plt.clf()
    plt.grid(True)
    plt.yscale('log')
    [plt.plot(xs, y, '{}-'.format(c)) for [y, c] in zip(ys, colors)]
    plt.show()
        

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) == 1:
        #display_tree()
        create_graph(28)
    else:
        show_individual(int(argv[1]))
        
        
        
        