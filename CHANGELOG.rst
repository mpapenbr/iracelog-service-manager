Changelog
=========


v0.6.1 (2023-03-11)
-------------------

New
~~~
- Prepare db for go-migrate. [mpapenbr]

Other
~~~~~
- Chore: make tox happy. [mpapenbr]


v0.6.0 (2023-01-22)
-------------------

New
~~~
- Provide version information for racelogger compatibilty check (#18)
  [mpapenbr]

Other
~~~~~
- Doc: link to overall documentation. [mpapenbr]
- Build: updated github actions + create release event. [mpapenbr]

  Fixes #9
  Fixes #12


v0.5.1 (2022-11-27)
-------------------

Fix
~~~
- Removed no longer needed ReplayInfo. [mpapenbr]


v0.5.0 (2022-11-26)
-------------------

New
~~~
- Compute avg laptimes over time (#14) [mpapenbr]
- Bulk speedmap data for replays #13. [mpapenbr]

Changes
~~~~~~~
- Preparations for copy event (#16) [mpapenbr]

Other
~~~~~
- Chore: cleanup, updated documentation. [mpapenbr]
- Chore: bump python to 3.10 for readthedocs. [mpapenbr]
- Chore: gha cache key, fix for Dockerfile. [mpapenbr]
- Chore: use github cache. [mpapenbr]
- Chore: use locked dependencies for github actions. [mpapenbr]
- Build: updated main dependencies. [mpapenbr]


v0.4.0 (2022-10-31)
-------------------

New
~~~
- Compute pit lane length for existing data (#10) [mpapenbr]

Changes
~~~~~~~
- TrackPitSpeed in trackdata. [mpapenbr]

Other
~~~~~
- Chore: removed check from standard tox env. [mpapenbr]

  Last chance for this env. Currently complains only in github actions.


v0.3.1 (2022-10-16)
-------------------

Fix
~~~
- Changed cardata topic. [mpapenbr]


v0.3.0 (2022-10-16)
-------------------

New
~~~
- Support for speedmap and driver data #7. [mpapenbr]
- Support for speedmap and driver data #7. [mpapenbr]

Changes
~~~~~~~
- Renamed driver data to car data. [mpapenbr]

Fix
~~~
- Adjusted test to new state_delta enum value. [mpapenbr]

Other
~~~~~
- Support for speedmap and driver data Fixes #7. [mpapenbr]


v0.2.4 (2022-04-16)
-------------------

Changes
~~~~~~~
- Additional rpc. [mpapenbr]

Fix
~~~
- Delta data composition (issue #1) [mpapenbr]


v0.2.3 (2022-02-19)
-------------------

Fix
~~~
- Store pit data for tracks (#5) [mpapenbr]


v0.2.2 (2021-12-04)
-------------------

New
~~~
- Added wait-for-it.sh script to image. [mpapenbr]


v0.2.0 (2021-12-04)
-------------------

New
~~~
- Check if crossbar server is ready upfront (helpful for docker)
  [mpapenbr]


v0.1.5 (2021-12-03)
-------------------

Changes
~~~~~~~
- Process extra event data. [mpapenbr]


v0.1.0 (2021-11-28)
-------------------

New
~~~
- Reworked wamp endpoints. [mpapenbr]
- Database access. [mpapenbr]
- Manager commands. [mpapenbr]
- Register events. [mpapenbr]

Changes
~~~~~~~
- Overview revisited. [mpapenbr]


v0.0.0 (2021-10-24)
-------------------
- Add initial project skeleton. [mpapenbr]


