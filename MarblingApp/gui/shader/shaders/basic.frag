#version 330

uniform int debug_mode;
in vec3 v_color;

out vec4 fragColor;

void main()
{
    if (debug_mode == 1)
        fragColor = vec4(1, 0, 0, 1.0);
    else
        fragColor = vec4(v_color, 1.0);
}