#version 330

in vec2 v_uv;
out vec4 f_color;

uniform sampler2D scene;

vec3 glow(float offset) {
    vec3 glow = vec3(0.0);

    glow += texture(scene, v_uv + vec2(offset, 0)).rgb * 0.25;
    glow += texture(scene, v_uv + vec2(-offset, 0)).rgb * 0.25;
    glow += texture(scene, v_uv + vec2(0, offset)).rgb * 0.25;
    glow += texture(scene, v_uv + vec2(0, -offset)).rgb * 0.25;

    vec3 base = texture(scene, v_uv).rgb;

    return base + glow;
}


void main() {
    vec3 col = texture(scene, v_uv).rgb;
//
    //float brightness = max(max(col.r, col.g), col.b);


    //// Glow threshold
    //if (brightness > 0.6) {
    //    glow = col;
    //}

    // Fake blur (cheap bloom)

    // Additive glow
    f_color = vec4(glow(0.002), 1.0);


}