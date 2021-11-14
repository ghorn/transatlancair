#include "stl.hpp"

#define GLM_ENABLE_EXPERIMENTAL

#include <fstream>
#include <glm/gtx/normal.hpp>
#include <cstring>
#include <iostream>
#include <unordered_map>

#include "src/meshtools/hash.hpp"

void SaveBinarySTL(
    const std::string &path,
    const std::vector<glm::vec3> &points,
    const std::vector<glm::ivec3> &triangles)
{
    // TODO: properly handle endian-ness
    const uint64_t numBytes = triangles.size() * 50 + 84;
    char *dst = (char *)calloc(numBytes, 1);

    const uint32_t count = static_cast<uint32_t>(triangles.size());

    // Check for overflow. Quit if num triangles too big.
    if (triangles.size() != static_cast<size_t>(count)) {
      std::cerr << "Error: too many triangles to represent as uint32 (" << triangles.size() << ")" << std::endl;
      exit(1);
    }

    memcpy(dst + 80, &count, 4);

    for (uint32_t i = 0; i < triangles.size(); i++) {
        const glm::ivec3 t = triangles[i];
        const glm::vec3 p0 = points[static_cast<uint64_t>(t.x)];
        const glm::vec3 p1 = points[static_cast<uint64_t>(t.y)];
        const glm::vec3 p2 = points[static_cast<uint64_t>(t.z)];
        const glm::vec3 normal = glm::triangleNormal(p0, p1, p2);
        const uint64_t idx = 84 + i * 50;
        memcpy(dst + idx, &normal, 12);
        memcpy(dst + idx + 12, &p0, 12);
        memcpy(dst + idx + 24, &p1, 12);
        memcpy(dst + idx + 36, &p2, 12);
    }

    std::fstream file(path, std::ios::out | std::ios::binary);
    file.write(dst, static_cast<int64_t>(numBytes));
    file.close();

    free(dst);
}

void ReadBinarySTL(
    const std::string &path,
    std::vector<glm::vec3> &points,
    std::vector<glm::ivec3> &triangles)
{
  std::ifstream is(path, std::ifstream::binary);
  if (!is) {
    std::cerr << "Error opening " << path << ".";
    std::exit(1);
  }

  std::unordered_map<glm::vec3, int32_t> point_map;

  // 80 bytes header (ignored)
  char buffer[80];
  is.read(buffer, 80);

  // number of triangles
  uint32_t num_triangles = 0;
  is.read(reinterpret_cast<char*>(&num_triangles), sizeof(uint32_t));
  
  // read each triangle
  int64_t count = 0;
  while (is) {
    // Read and discard normal.
    glm::vec3 normal;
    static_assert(sizeof(normal) == 3*sizeof(float));
    is.read(reinterpret_cast<char*>(&normal), 3*sizeof(float));

    // Read three vertices.
    glm::vec3 vertices[3];
    static_assert(sizeof(vertices) == 9*sizeof(float));
    is.read(reinterpret_cast<char*>(vertices), 9*sizeof(float));

    // Record the triangle
    int32_t point_indices[3];
    for (int k=0; k<3; k++) {
      const glm::vec3 &point = vertices[k];

      if (point_map.find(point) != point_map.end()) {
        // If point is already known, reference it.
        point_indices[k] = point_map.at(point);
      } else {
        // If point is not known, insert it.
        const int32_t new_index = static_cast<int32_t>(points.size());
        point_indices[k] = new_index;
        points.push_back(point);
        point_map.insert({point, new_index});
      }
    }
    glm::ivec3 triangle_index = {point_indices[0], point_indices[1], point_indices[2]};
    triangles.push_back(triangle_index);

    // Read attribute byte count. According to wikipedia this should always be zero.
    uint16_t attribute_byte_count;
    is.read(reinterpret_cast<char*>(&attribute_byte_count), sizeof(uint16_t));
    assert(attribute_byte_count == 0);

    // increment count
    count++;
  }

  const int64_t expected_count = static_cast<int64_t>(num_triangles);
  if (count != expected_count) {
    std::cerr << "Got wrong number of triangles. Expected " << count << ", got " << expected_count << std::endl;
    //std::exit(1);
  }

  is.close();
}
