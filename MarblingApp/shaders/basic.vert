#version 330

in vec2 in_vert;
in vec3 in_color;

out vec3 v_color;

float rand(vec2 co)
{
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main()
{
    gl_Position = vec4(in_vert, 0.0, 1.0);
    v_color = in_color;// vec3(rand(in_vert), in_color.g, rand(in_vert));
}