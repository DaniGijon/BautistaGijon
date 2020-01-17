#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Trawlnet.ice')
import miModulo


class OrchestratorI(miModulo.Orchestrator):
    n=0
    downloader = None
    
    def downloadTask(self,url,current=None):
        print("{0}: {1}".format(self.n, url[0:]))
        sys.stdout.flush()
        self.n += 1
        salida = self.downloader.addDownloadTask(url)
       # salida = (miModulo.FileInfo('miau0','h0'))
        return salida

    def getFileList(self,current=None):
        #lista de canciones
        listaCanciones = (miModulo.FileInfo('s0','h0'),miModulo.FileInfo('s1','h1'),)
        song2 = (miModulo.FileInfo('s2','h2'),)
        listaCanciones = listaCanciones+song2
        
        #song1 = {'name': "nombreSong1", 'hash': "hash1"}
        #song2 = {'name' : 'nombresong2', 'hash' : 'hash2'}
       # listaSongs.append(song2)
        #listaSongs = [("s0","h0")]   
                	        
       # print("{0}: {1}".format(self.n, listaSongs))
       # sys.stdout.flush()
       # self.n += 1
        return listaCanciones
            
class Orchestrator(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = OrchestratorI()
        
        adapter = broker.createObjectAdapter("OrchestratorAdapter")
        
    
        proxy = self.communicator().stringToProxy(argv[1])
        
        proxyy = adapter.add(servant,broker.stringToIdentity("orchestrator1"))
        print(proxyy, flush=True)
        
       # downloader 
        downloader = miModulo.DownloaderPrx.checkedCast(proxy)

        if not downloader:
            raise RuntimeError('Invalid proxy')
        
        
        servant.downloader = downloader

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        
        return 0


sys.exit(Orchestrator().main(sys.argv))
