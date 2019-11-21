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
        print("{0}: {1}".format(self.n, url))
        sys.stdout.flush()
        self.n += 1
        salida = self.downloader.addDownloadTask(url)
        
        return salida


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
