# map-pinchpoints
Library for finding pinchpoints for hikers from OSM data

## User story

**As a** cyclist with a 3 hour handicap, **I want** to identify pinchpoints for hikers travelling from a start location to an end location on specified areas of map **so that** I can catch them and get points, whilst losing them points.

## Usage

```
    python alpha.py
```

## TO DO:

### Known bugs
- The algorithm drops half of loops because the network can't distinguish them
- No route around something should make it a pinchpoint (at least in small networks)

### Additional features:
- Location input
- Portablility
- Multiple maps
- Draw the whole pinchpoint segment
- Cache sections of map
- YAML config?