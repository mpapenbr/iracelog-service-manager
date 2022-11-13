Architecture
============

The overall picture looks like this

.. image:: arch.drawio.svg

Upon connecting to the local iRacing instance the Racelogger registers with the backend with a unique id (this is generated via the current iRacing weekend info from telemetry).

The manager announces the provider changes  on the `manager.provider` topic. 

The analysis and archive components listen to this topic and prepare themselves 
to receive data from the live topics associated with announced key (for example `live.state.{key}`) to which the Racelogger will post its data. 

At the end of recording the Racelogger calls the `remove_provider` endpoint. The manager in turn announces this event on the topic `manager.provider`

Endpoints
---------

.. list-table:: 
    :widths: auto
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
   
    * - racelog.admin.
      - used by admin CLI
      - admin
      - call, register, publish, subscribe

Crossbar
--------

The following snippet can be used as a template for a crossbar server.

.. literalinclude:: crossbar.config
  :language: json
  :linenos: 

