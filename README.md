Warning: This is a work in progress.

The purpose of this repository is to visualize my recent single-engine Atlantic crossing.

The command 

> ./bazelisk run //:plot_map

may or may not produce:

![alt text](https://github.com/ghorn/transatlancair/blob/main/readme/map_with_tracks.png?raw=true)

This is a Gnomic projection so straight lines are great circle paths.

When the above command doesn't work, it's probably because you need to run `get_dem_data.sh` which gets *some but not all* of the DEMs.
Comment/uncomment the relevant sections at the top of `BUILD.bazel`.

I want to make a 3d model of the earth with these tracks overlaid. I'm using https://github.com/fogleman/hmm to trianguate heightmaps found in various places. Here is a WIP:

![alt text](https://github.com/ghorn/transatlancair/blob/main/readme/copernicus.png?raw=true)

> ./bazelisk build //...

should produce that and other STLs.

I got distracted and did these topobathymetries of the SF bay as well:

![alt text](https://github.com/ghorn/transatlancair/blob/main/readme/sfbay_reliefs.png?raw=true)
