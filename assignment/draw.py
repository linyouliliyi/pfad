import matplotlib.pyplot as plt

def draw_scatter(norads, alts):
    plt.scatter(norads, alts, s=15)
    plt.title('Starlink Altitude distribution of satellites')
    plt.xlabel('Norad')
    plt.ylabel('Alt(km)')
    plt.show()

    