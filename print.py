f1= open(r"out/h1.txt",'r')
f1file=f1.readlines()
out1=f1file[-2].split(' ')
print('Throughput ='+out1[-2]+'Mbps')

f2=open(r"out/h7.txt",'r')
f2file=f2.readlines()
ploss=f2file[-2].split(',')[2]
print(ploss)

rtt=f2file[-1].split('=')[3].split("/")
lat=rtt[1]/2
print("Latency=", lat)
