#!/usr/bin/python

"""Sample file for SUMO

***Requirements***:

sumo
sumo-gui"""

import os
import timer

from mininet.node import Controller
from mininet.log import setLogLevel, info
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI_wifi
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd
from mn_wifi.wmediumdConnector import interference

interval = 5

def topology():

    "Create a network."
    net = Mininet_wifi(controller=Controller, accessPoint=UserAP,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    cars = []
    stas = []
    for x in range(0, 10):
        cars.append(x)
        stas.append(x)
    for x in range(0, 10):
        cars[x] = net.addCar('car%s' % (x),
                             wlans=1, ip='10.0.0.%s/8' % (x + 1))

    rsus = []

    e1 = net.addAccessPoint('e1', ssid='vanet-ssid', mac='00:00:00:11:00:01',
                            mode='g', channel='1', passwd='123456789a',
                            encrypt='wpa2', position='3279.02,3736.27,0')
    e2 = net.addAccessPoint('e2', ssid='vanet-ssid', mac='00:00:00:11:00:02',
                            mode='g', channel='6', passwd='123456789a',
                            encrypt='wpa2', position='2320.82,3565.75,0')
    e3 = net.addAccessPoint('e3', ssid='vanet-ssid', mac='00:00:00:11:00:03',
                            mode='g', channel='11', passwd='123456789a',
                            encrypt='wpa2', position='2806.42,3395.22,0')
    e4 = net.addAccessPoint('e4', ssid='vanet-ssid', mac='00:00:00:11:00:04',
                            mode='g', channel='1', passwd='123456789a',
                            encrypt='wpa2', position='3332.62,3253.92,0')
    e5 = net.addAccessPoint('e5', ssid='vanet-ssid', mac='00:00:00:11:00:05',
                            mode='g', channel='6', passwd='123456789a',
                            encrypt='wpa2', position='2887.62,2935.61,0')
    e6 = net.addAccessPoint('e6', ssid='vanet-ssid', mac='00:00:00:11:00:06',
                            mode='g', channel='11', passwd='123456789a',
                            encrypt='wpa2', position='2351.68,3083.40,0')

    rsus.append(e1)
    rsus.append(e2)
    rsus.append(e3)
    rsus.append(e4)
    rsus.append(e5)
    rsus.append(e6)

    c1 = net.addController('c1')

    info("*** Setting bgscan\n")
    net.setBgscan(signal=-45, s_inverval=5, l_interval=10)

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=2)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    net.addLink(e1, e2)
    net.addLink(e2, e3)
    net.addLink(e3, e4)
    net.addLink(e4, e5)
    net.addLink(e5, e6)

    net.useExternalProgram(program=sumo, port=8813,
                           config_file='bolognaringway.sumo.cfg')

    net.plotGraph(max_x=5000, max_y=5000)

    info("*** Starting network\n")
    net.build()
    c1.start()
    e1.start([c1])
    e2.start([c1])
    e3.start([c1])
    e4.start([c1])
    e5.start([c1])
    e6.start([c1])


    i = 201
    for sw in net.carsSW:
        sw.start([c1])
        os.system('ip addr add 10.0.0.%s dev %s' % (i, sw))
        i += 1

    i = 1
    j = 2
    for car in cars:
        car.setIP('192.168.0.%s/24' % i, intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % i, intf='%s-eth1' % car)
        car.cmd('ip route add 10.0.0.0/8 via 192.168.1.%s' % j)
        i += 2
        j += 2

    i = 1
    j = 2
    for carsta in net.carsSTA:
        carsta.setIP('10.0.0.%s/24' % i, intf='%s-mp0' % carsta)
        carsta.setIP('192.168.1.%s/24' % j, intf='%s-eth2' % carsta)
        # May be confuse, but it allows ping to the name instead of ip addr
        carsta.setIP('10.0.0.%s/24' % i, intf='%s-wlan0' % carsta)
        carsta.cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')
        i += 1
        j += 2

    for carsta1 in net.carsSTA:
        i = 1
        j = 1
        for carsta2 in net.carsSTA:
            if carsta1 != carsta2:
                carsta1.cmd('route add -host 192.168.1.%s '
                            'gw 10.0.0.%s' % (j, i))
            i += 1
            j += 2

    t = timer.MyTimer(interval)
    t.set_interval(show_cars_positions,{"cars":cars,"rsus":rsus})

    info("*** Running CLI\n")
    CLI_wifi(net)

    info("*** Stopping network\n")
    t.stop_intervals()
    net.stop()

def show_cars_positions(args):
    tmp = None
    i = 0
    for car in args["cars"]:
        tmp = car.name + " distances"
        print ("%s associated to %s" % (car.name,car.params['associatedTo']))
        for rsu in args["rsus"]:
            tmp += " from %s is %s" % (rsu.name ,rsu.get_distance_to(car))
        print (tmp)
    print ("*********************************************************")

if __name__ == '__main__':
    setLogLevel('info')
    topology()
