#version 420

in vec3 vertex;
in vec3 normal;
in vec3 color;
out vec4 fragment_color;

uniform float light_ambient_weight;
uniform vec3 light_ambient_color;

uniform vec3 light_pos;
uniform vec3 light_dir;
uniform vec3 light_color;
uniform float light_glare;   // Spectacular weight

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    // ambient
    vec3 ambient = light_ambient_weight * light_ambient_color;

    // diffuse 
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - vertex);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * light_color;

    // specular
    vec3 viewDir = normalize(-vertex);
    vec3 reflectDir = reflect(-light_dir, norm); 
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 16);
    vec3 specular = light_glare * spec * light_color;  

    vec3 result = (ambient + diffuse + specular) * color;
    fragment_color = vec4(result, 1.0);
}
