import matplotlib.pyplot as plt
import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: python <data filename> <output graph filename>')
        exit(0)
        
    with open(sys.argv[1]) as data_file:    
        data = json.load(data_file)
        
        xs = [i for i in range(len(data[0]))]     # number of generations of the first class (and all of the other classes)
        ys = [[-data[c][i][0][3] for i in range(len(data[c]))] for c in range(len(data))]
        colors = ['r', 'b', 'g', 'c', 'y', 'm', 'k']
        plt.clf()
        plt.grid(True)
        plt.yscale('log')
        [plt.plot(xs, y, '{}-'.format(c)) for [y, c] in zip(ys, colors)]

        # plt.show()
        plt.savefig('images/' + sys.argv[2])
        