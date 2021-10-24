Architecture
============

Endpoints
---------

.. list-table:: Crossbar endpoints
    :widths: 10 10 10 10
    :header-rows: 1

    * - Prefix 
      - Description    
      - User 
      - Access

    * - racelog.public.
      - used for public access (mainly frontend)
      - anonymous
      - call, subscribe
    
    * - racelog.dataprovider.
      - used by racelogger to publish race data
      - datapublisher
      - call, publish, subscribe

    * - racelog.manager.
      - used by the backend apps
      - backend
      - call, register, publish, subscribe





