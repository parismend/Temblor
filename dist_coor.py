import geopy as gp
from geopy.distance import vincenty

def op_base(file):
    base = []
    with open (file, 'r') as sq:
        base = sq.read()

def cal_dist(lat,long):
    cerc = []
    for x in base:
        dist = vincenty((base[x][12],base[x][13]), (lat,long)).meters
        if dist < 100:
            cerc.append(base[x])
    return cerc

if __name__ == '__main__':
    op_base()
    aaa = cal_dist()
