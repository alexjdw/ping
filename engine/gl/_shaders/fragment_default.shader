#version 420
in vec3 color;

void main() {
    gl_FragColor = vec4(color.xyz, 1.);
}