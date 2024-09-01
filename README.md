# map-pinchpoints
Library for finding pinchpoints for hikers from OSM data

## User story

**As a** cyclist with a 3 hour handicap, **I want** to identify pinchpoints for hikers travelling from a start location to an end location on specified areas of map **so that** I can catch them and get me points, whilst losing them points.

## Usage

Config lives in `config.yaml`

```
$ python run_pipeline.py
```

Copy changes to `pinchpoints.html` out to `docs/index.html` so they're accessible in GH Pages

## TO DO:

### Additional features:
- No route around something could make it a pinchpoint (at least in small networks)
- Typing throughout
- Break out graph manipulation code to separate file
- File renaming
- Less hacky/more polite data download
- Add testing
