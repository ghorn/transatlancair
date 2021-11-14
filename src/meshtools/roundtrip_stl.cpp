#include <string>
#include <getopt.h>
#include <cassert>
#include <iostream>
#include <fstream>
#include <vector>
#include <glm/glm.hpp>

#include "src/meshtools/stl.hpp"

// Usage: ./trim_bottom inputpath outputpath
int32_t main(int32_t argc, char *argv[]) {
  // Parse flags.
  if (argc != 3) {
    fprintf(stderr, "Need 2 command line arguments, input and output\n");
    exit(1);
  }
  std::string input_path = argv[1];
  std::string output_path = argv[2];
  assert(input_path.size() != 0);
  assert(output_path.size() != 0);

  // Read inputs.
  std::vector<glm::vec3> vertices;
  std::vector<glm::ivec3> triangles;
  LoadStl(input_path, &vertices, &triangles);

  // Write outputs.
  SaveStl(output_path, vertices, triangles);
}