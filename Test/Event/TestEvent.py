


from multiprocessing import Process, Pipe
import EventTest

recCon, sendCon = Pipe(duplex=False)

def initServer(s):
     EventTest.creatEvent(s)



p = Process(target=initServer, args=(recCon,))
p.start()

sendCon.send('11')
print 'send 1'
sendCon.send('22')
sendCon.send('33')
sendCon.send('44')


