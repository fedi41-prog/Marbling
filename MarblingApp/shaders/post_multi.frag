#version 330

in vec2 v_uv;
out vec4 f_color;

uniform sampler2D scene;

float rand(vec2 co)
{
    return fract(sin(dot(co.xy ,vec2(12.9898,78.233))) * 43758.5453);
}

float diagonalPattern(vec2 uv)
{
    float spacing = 10.0; // Abstand zwischen Linien

    float v = mod(uv.x + uv.y, spacing);

    return v < 5.0 ? 1.0 : 0.0; // Linienbreite 2 Pixel
}

float diff(vec3 col1, vec3 col2) {
    return (abs(col1.r-col2.r)+abs(col1.g-col2.g)+abs(col1.b-col2.b))/3;
}

vec3 glow2(float offset) {
    vec3 glow = vec3(0.0);

    glow += texture(scene, v_uv + vec2(offset, 0)).rgb * 0.25;
    glow += texture(scene, v_uv + vec2(-offset, 0)).rgb * 0.25;
    glow += texture(scene, v_uv + vec2(0, offset)).rgb * 0.25;
    glow += texture(scene, v_uv + vec2(0, -offset)).rgb * 0.25;

    vec3 base = texture(scene, v_uv).rgb;

    return base + glow;
}

vec3 glow(float a, int b, float c) {


    vec3 color = texture(scene, v_uv).rgb;


    for (int i = -b; i <= b; i++) {
        for (int j = -b; j <= b; j++) {
            color += texture(scene, v_uv + vec2(i*a, j*a)).rgb/c;
        }
    }

    return color;
}

vec3 sharpen(float a, int b, float c) {


    vec3 color = texture(scene, v_uv).rgb;

    for (int i = -b; i <= b; i++) {
        for (int j = -b; j <= b; j++) {
            color -= diff(texture(scene, v_uv).rgb, texture(scene, v_uv + vec2(i*a, j*a)).rgb);
        }
    }

    return color;
}


vec3 test() {
    vec3 color = texture(scene, v_uv).rgb;

    float brightness = max(max(color.r, color.g), color.b);

    if (brightness < 0.2) return color;

    float r = rand(v_uv);
    color = color + vec3(r,r,r)/3;

    return color;
}
vec3 blur(float a, int b, float c) {


    vec3 color = texture(scene, v_uv).rgb;

    vec3 g = color;

    for (int i = -b; i <= b; i++) {
        for (int j = -b; j <= b; j++) {
            g += texture(scene, v_uv + vec2(i*a, j*a)).rgb;
        }
    }

    g /= b*b*c;

    return g;
}
void main() {
    vec3 col = texture(scene, v_uv).rgb;

    float brightness = max(max(col.r, col.g), col.b);
    vec2 pos = gl_FragCoord.xy;

    float pattern1 = diagonalPattern(pos);


    if (v_uv.y < 0.5)
        if (v_uv.x < 0.5)
            //f_color = vec4(brightness, brightness, brightness, 1);
            f_color = vec4(blur(0.002, 7, 5), 1);
        else
            f_color = vec4(glow(0.002, 5, 120), 1);
    else
        if (v_uv.x < 0.5)
            f_color = vec4(col, 1);
        else {
            //f_color = vec4(vec3(1,1,1)-col, 1);
            col = sharpen(0.001, 1, 50);
            if (brightness > 0.2)
                col -= pattern1;
            f_color = vec4(col, 1);

        }
}