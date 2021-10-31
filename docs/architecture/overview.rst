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





Migration
---------

Racelogger
^^^^^^^^^^


.. list-table:: Racelogger
    :widths: 10 10 10 
    :header-rows: 1

    * - Current
      - Access
      - New

    * - racelog.register_provider
      - call
      - racelog.dataprovider.register_provider
    
    * - racelog.remove_provider
      - call
      - racelog.dataprovider.remove_provider

    * - racelog.store_event_extra_data
      - call
      - racelog.dataprovider.provide_event_extra_data

Web
^^^

.. list-table:: Webfrontend (iRacelog)
    :widths: auto
    :header-rows: 1

    * - Current
      - Access       
      - New
      - Where
      - Description

    * - racelog.archive.event_info
      - call
      - racelog.public.get_event_info
      - load event
      - get info about selected event

    * - racelog.archive.events
      - call
      - racelog.public.get_events
      - startup
      - get list of stored events

    * - racelog.list_providers
      - call
      - racelog.public.list_providers
      - startup/request
      - get list of current race data providers


    * - racelog.get_track_info
      - call
      - racelog.public.get_track_info
      - load event
      - get info about track

    * - racelog.analysis.archive
      - call
      - racelog.public.archive.get_event_analysis
      - load event
      - get stored analysis data
    
    * - racelog.analysis.live
      - call
      - racelog.public.live.get_event_analysis
      - live
      - get current live analysis data
    
    * - racelog.state.{id}
      - topic
      - racelog.public.live.state.{id}
      - live
      - get current state from racelogger 
    
