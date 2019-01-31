#!/usr/bin/python

"""Sample file for SUMO

***Requirements***:

sumo
sumo-gui"""

import os
import timer
import filePlacement as fp
import requests as req
import networkx as nx

from anytree import AnyNode, RenderTree
from random import randint
from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

interval = 5
number_of_files=35
req_update_interval = 20
cache_update_interval=60
mobile_rsu_pos = 1
mobile_rsu_arr = [1]

def topology():

    "Create a network."
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating graph\n")
    G = nx.Graph()
    e = [('1', '2', 0.4), ('1', '3', 0.3), ('2', '4', 0.8), ('3', '4', 0.6),('2', '3', 1.2)]
    G.add_weighted_edges_from(e)

    
    info("*** Creating nodes\n")
    cars = []
    stas = []
    for x in range(0, 10):
        stas.append(x)


    cars = []
    for id in range(0, 10):
        cars.append(net.addCar('car%s' % (id+1), wlans=2, ip='10.0.0.%s/8' % (x + 1)))

    rsus = {}

    for i in range(0,4):
        for j in range(1,4):
            magic = (i*3 + j)
            channel = "%s" % (5*j-4)
            name = "e%s" % (magic)
            mac = "00:00:00:11:00:0%s"%(hex(magic)[2])

            if i % 2 == 0 :
                pos = "%d,%d,0" % ((j-1)*2000+1000,(i+1)*1000)
            else:
                pos = "%d,%d,0" % ((3-j)*2000,(i+1)*1000)

            rsu = net.addAccessPoint(name, ssid='vanet-ssid%s'%(magic), mac=mac, mode='g', channel=channel, position=pos)
            rsus["e%d" % (magic)] = rsu
            # print ("RSU%d, pos %s, channel %s" % (magic , pos, channel))


    c1 = net.addController('c1')

    info("*** file placement\n")
    X = fp.FilePlacement(number_of_caches=len(rsus),min_cache_size=10,number_of_files=number_of_files,max_cache_size=14)
    R = req.Requests(number_of_cars=10,min_req_size=5,max_req_size=10,number_of_files=number_of_files)


    # info("*** Setting bgscan\n")
    # net.setBgscan(signal=0, s_inverval=1, l_interval=10)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    for i in range(1,12):
        net.addLink("e%d"%(i), "e%d"%(i+1))

    net.useExternalProgram(program=sumo, port=8813,
                           config_file='bolognaringway.sumo.cfg')

    net.plotGraph(max_x=5000, max_y=5000)

    # net.startMobility(time=0)

    info("*** Starting network\n")
    net.build()
    c1.start()

    for i in rsus:
        rsus[i].start([c1])

    for car in cars:
        car.setIP('192.168.0.%s/24' % (int(cars.index(car))+1),
                  intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % (int(cars.index(car))+1),
                  intf='%s-mp1' % car)


    t = timer.MyTimer(interval)
    t2 = timer.MyTimer(req_update_interval)
    t3 = timer.MyTimer(cache_update_interval)
    t.set_interval(show_cars_positions,{"cars":cars,"rsus":rsus,"X":X,"R":R,"G":G})
    t2.set_interval(R.update_req,{})
    t3.set_interval(X.mobile_RSU,{"G":G})

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    t.stop_intervals()
    t2.stop_intervals()
    t3.stop_intervals()
    net.stop()
    os.system("sudo ps -aux | sudo grep sumo-gui | sudo awk '{print $2}' | sudo head -n 1 | sudo xargs kill")
    os.system("sudo mn -c")

def mobile_rsu(args):
    if len(mobile_rsu_arr) != 0 :
        mobile_rsu_pos = mobile_rsu_arr.pop()
        return

    root = AnyNode(id='1',cost=0,benefit=G.node['1']['benefit'])
    mrsu.mobile_RSU_path('1',G,2,root,root,'1')

    for pre, fill, node in RenderTree(root):
        print("%s%s:%s:%s" % (pre, node.id,node.benefit,node.cost))
    best_node = root
    for pre, fill, node in RenderTree(root):
        if best_node.benefit < node.benefit:
            best_node = node

    while best_node.parent is not None:
        mobile_rsu_pos.append(best_node.id)
        best_node = best_node.parent

def show_cars_positions(args):
    i = 0
    X = args["X"]
    R = args["R"]
    G = args["G"]
    rsus = args["rsus"]
    hits_arr = []
    reqs = []

    for i in range(0,4):
        hits_arr.append(0)
        reqs.append(0)

    for car in args["cars"]:
        if car.params['associatedTo'][0] is not "" :
            req_arr = R.get_car_req(int(car.name[3:]))
            hits = 0
            association = str(car.params['associatedTo'][0])

            if association is not "bgscan":
                sector = get_sector(int(association[1:]))-1
                hits = X.request_cache_hits(req_arr,int(association[1:]))
                if sector == mobile_rsu_pos:
                    hits = len(req_arr)
                reqs[sector] += len(req_arr)
                hits_arr[sector] += hits
                print ("%s associated to %s requested %s, hits %s" % (car.name,association,req_arr,float(hits)/len(req_arr)))

    for i in range(0,4):
        if (reqs[i] != 0 ):
            G.node[i+1]['benefit'] = reqs[i]
            print ("sector %s, hits ratio %s" % (i,float(hits_arr[i])/reqs[i]))



        # if rsus[rsu].get_distance_to(car) < min_dis :
        # min_dis = rsus[rsu].get_distance_to(car)

        #print ("minimum RSU is : %s distance %s" % (min_rsu,min_dis))
    # R.show_all()
    print ("*********************************************************")

def get_sector(rsu_id):
    if rsu_id == 1 or rsu_id == 6 or rsu_id == 5 :
        return 3
    if rsu_id == 2 or rsu_id == 3 or rsu_id == 4 :
        return 4
    if rsu_id == 7 or rsu_id == 11 or rsu_id == 12 :
        return 1
    if rsu_id == 8 or rsu_id == 9 or rsu_id == 10 :
        return 2


if __name__ == '__main__':
    setLogLevel('info')
    topology()
