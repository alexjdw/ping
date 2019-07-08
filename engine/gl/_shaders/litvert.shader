#version 420
layout (location=0) in vec3 vertex_attrib;
// in vec3 texcoord_attrib;
layout (location=1) in vec3 normal_attrib;
layout (location=2) in vec3 color_attrib;
out vec3 vertex;
out vec3 normal;
out vec3 color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    vertex = vec3(projection * view * model * vec4(vertex_attrib, 1));
    gl_Position = vec4(vertex, 1);
    normal = normal_attrib;
    color = color_attrib;
}
