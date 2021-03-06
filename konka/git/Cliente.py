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
        
        url = argv[2]
        if len(sys.argv) > 3:
            opcion = argv[3]
            #dependiendo de la opcion, llamara a una accion o a otra
            if opcion == 'download':
                d = orchestrator.downloadTask(url)
                print(d)
            elif opcion == 'transfer':    
                orchestrator.getFile(url)
        else:
            #si no hay opcion, pedirá la lista de canciones
            songList = orchestrator.getFileList()
            print(songList)
     #       orchestrator.downloadTask(url, opcion)
      #  else:
       #     orchestrator.downloadTask(url, "listar")
       
        return 0


sys.exit(Cliente().main(sys.argv))
