#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice
Ice.loadSlice('Trawlnet.ice')
import miModulo

class Cliente(Ice.Application):
    def run(self, argv):
    
        proxy = self.communicator().stringToProxy(argv[1])
        
        orchestrator = miModulo.OrchestratorPrx.checkedCast(proxy)

        if not orchestrator:
            raise RuntimeError('Invalid proxy')

        orchestrator.downloadTask('Hi!!')

        return 0


sys.exit(Cliente().main(sys.argv))
