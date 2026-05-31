#version 330

in vec2 in_pos;
out vec2 v_uv;

float rand(vec2 co)
{
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

void main() {
    v_uv = in_pos * 0.5 + 0.5;



    gl_Position = vec4(in_pos, 0.0, 1.0);
}