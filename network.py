#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call


def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='192.168.0.0/16',
                   link=TCLink)

    info('*** Adding controller\n')
    c0 = net.addController(name='c0',
                           controller=RemoteController,  #Added remote controller (floodlight) 
                           ip='192.168.56.3',
                           protocol='tcp',
                           port=6653)

    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch)
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch)
    s6 = net.addSwitch('s6', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s9 = net.addSwitch('s9', cls=OVSKernelSwitch)
    s10 = net.addSwitch('s10', cls=OVSKernelSwitch)
    s11 = net.addSwitch('s11', cls=OVSKernelSwitch)
    s12 = net.addSwitch('s12', cls=OVSKernelSwitch)
    s13 = net.addSwitch('s13', cls=OVSKernelSwitch)
    s14 = net.addSwitch('s14', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.56.11', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.56.12', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.56.13', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.56.14', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='192.168.56.15', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='192.168.56.16', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='192.168.56.17', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='192.168.56.18', defaultRoute=None)


    info( '*** Add links with bandwidth, delay and packetloss values\n')
    net.addLink(s1, h1, bw=15, delay= '1ms', loss=1)
    net.addLink(s1, s2, bw=15, delay= '1ms', loss=1)
    net.addLink(s1, s4, bw=15, delay= '1ms', loss=1)
    net.addLink(s2, s3, bw=15, delay= '1ms', loss=1)
    net.addLink(s3, s5, bw=15, delay= '1ms', loss=1)
    net.addLink(s5, s6, bw=15, delay= '1ms', loss=1)
    net.addLink(s6, h2, bw=15, delay= '1ms', loss=1)
    net.addLink(s2, s7, bw=15, delay= '1ms', loss=1)
    net.addLink(s7, s8, bw=15, delay= '1ms', loss=1)
    net.addLink(s8, h3, bw=15, delay= '1ms', loss=1)
    net.addLink(s7, s9, bw=15, delay= '1ms', loss=1)
    net.addLink(s9, s10, bw=15, delay= '1ms', loss=1)
    net.addLink(s10, s11, bw=15, delay= '1ms', loss=1)
    net.addLink(s11, s12, bw=15, delay= '1ms', loss=1)
    net.addLink(s12, h4, bw=15, delay= '1ms', loss=1)
    net.addLink(s10, h5, bw=15, delay= '1ms', loss=1)
    net.addLink(s9, s13, bw=15, delay= '1ms', loss=1)
    net.addLink(s13, s14, bw=15, delay= '1ms', loss=1)
    net.addLink(s14, h7, bw=15, delay= '1ms', loss=1)
    net.addLink(s14, h8, bw=15, delay= '1ms', loss=1)
    net.addLink(s13, h6, bw=15, delay= '1ms', loss=1)


    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([c0])
    net.get('s2').start([c0])
    net.get('s3').start([c0])
    net.get('s4').start([c0])
    net.get('s5').start([c0])
    net.get('s6').start([c0])
    net.get('s7').start([c0])
    net.get('s8').start([c0])
    net.get('s9').start([c0])
    net.get('s10').start([c0])
    net.get('s11').start([c0])
    net.get('s12').start([c0])
    net.get('s13').start([c0])
    net.get('s14').start([c0])


    info( '*** Post configure switches and hosts\n')
    hosts = net.hosts
    server = h1
    client= h7
    outfiles, capfiles, errfiles = {}, {}, {}
    

    for h in hosts:
        outfiles[ h ] = './out/%s.txt' % h.name # to store the output 
        capfiles[ h ] = './cap/%s.txt' % h.name 
        errfiles[ h ] = './err/%s.err' % h.name

    server.cmdPrint('iperf -s -u') 
    client.cmdPrint('iperf -c 192.168.56.11 -u -b 6M -e -t 100', '>', outfiles[server], '2>', errfiles[server]) #To run UDP protocol with 6Mbps bandwidth for 100 seconds
    server.cmdPrint('ping -w 100 192.168.56.17', '>', outfiles[client], '2>', errfiles[client]) #To run ping that uses ICMP for 100 seconds
    

    net.stop()

    f1= open(r"out/h1.txt",'r')
    f1file=f1.readlines()
    out1=f1file[-2].split(' ')
    print('Throughput ='+out1[-8]+'Mbps')
    print('Jitter='+out1[-4]+'ms')
   
    f2=open(r"out/h7.txt",'r')
    f2file=f2.readlines()
    ploss=f2file[-2].split(',')[2]
    print(ploss)

    rtt=f2file[-1].split('=')[1].split("/")
    lat=float(rtt[1]/2)
    print("Latency=", lat)

    

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

