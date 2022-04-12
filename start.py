

import importorinstall

importorinstall.package('selenium')
importorinstall.package('webdriver_manager')
importorinstall.package('CloudFlare')
importorinstall.package('mysql-connector-python')

import main

while(main.CheckIPv4() == 'reconnect_ok'):
    main.CheckIPv4()