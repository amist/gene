import matplotlib.pyplot as plt
import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python <data filename> <output graph filename>')
        exit(0)
        
    with open(sys.argv[1]) as data_file:    
        data = json.load(data_file)
        # data          = [run, run, run, ...]
        # where:
        # run           = [generation, generation, generation, ...]
        # generation    = [best_individual, another_individual, another_individual, ...]
        # individual    = (index, parent1_index, parent2_index, fitness_value)
        
        # TODO: handle runs with varying lengths
        xs = [i for i in range(len(data[0]))]     # number of generations of the first class (and all of the other classes)
        
        # len(data)         = number of runs (usually number of classes which have been compared)
        # c                 = index of run
        # data[c]           = generations of run c
        # len(data[c])      = number of generations of run c
        # data[c][i]        = list of individuals in generation i of run c
        # data[c][i][0]     = the best individual in generation i of run c - tuple of (index, parent1_index, parent2_index, fitness_value)
        # data[c][i][0][3]  = fitness value of the best individual in generation i of run c
        ys = [[-data[c][i][0][3] for i in range(len(data[c]))] for c in range(len(data))]
        colors = ['r', 'b', 'g', 'c', 'y', 'm', 'k']
        plt.clf()
        plt.grid(True)
        plt.yscale('log')
        
        # plt.gca().set_ylim([1e-300, 1e16])
        
        [plt.plot(xs, y, '{}-'.format(c)) for [y, c] in zip(ys, colors)]

        # plt.show()
        plt.savefig('images/' + sys.argv[2])
        