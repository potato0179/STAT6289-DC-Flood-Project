
# NOAA MRMS Data Availability Summary

## Data Source

- Product: NOAA MRMS MultiSensor_QPE_01H_Pass2
- Archive: Iowa State University MTArchive
- Temporal resolution: Hourly precipitation accumulation
- Units: mm
- Study area: Washington, DC and surrounding region

## Event Coverage

A total of 125 documented flood events were examined.

- Complete MRMS coverage: 26 events
- Partial MRMS coverage: 1 event
- Missing MRMS coverage: 97 events
- Zero-duration event: 1 event

The initial archive-availability analysis counted 818 hourly observations, including one zero-duration event. The final event-based coverage analysis excludes this event, resulting in 817 expected event-hours, of which 128 were available.

## Archive File Availability

Of 316 candidate hourly files checked:

- HTTP 200: 126 files
- HTTP 404: 190 files

An additional 498 planned files occurred before the
preliminary archive coverage cutoff of October 2014.

HTTP 404 indicates that the requested file was not
available at the tested archive URL. It does not prove
that equivalent observations are unavailable elsewhere.

## Partially Covered Event

Event ID: event_107

Event period:
2021-09-16 19:53 UTC to 2021-09-17 01:41 UTC

- Expected hourly files: 7
- Available hourly files: 4
- Missing hourly files: 3
- Coverage: 57.14%

The following hourly files returned HTTP 404:

- 2021-09-16 20:00 UTC
- 2021-09-16 21:00 UTC
- 2021-09-16 22:00 UTC

## Limitations

Availability was assessed using the selected
Iowa State University MTArchive product path.

The results describe file-level temporal coverage
rather than complete pixel-level data quality.

Missing observations were not replaced with zero
precipitation.

The analysis does not establish that NOAA MRMS
data are unavailable from all possible archives.
