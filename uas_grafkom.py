import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# --- DATA OBJEK ---
vertices_cube = [[1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1], [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1]]
edges_cube = [(0,1), (1,2), (2,3), (3,0), (4,5), (5,7), (7,6), (6,4), (0,4), (1,5), (2,7), (3,6)]
vertices_sq = [(0.5, 0.5, 0), (-0.5, 0.5, 0), (-0.5, -0.5, 0), (0.5, -0.5, 0)]

def draw_cube():
    glBegin(GL_LINES)
    for edge in edges_cube:
        for vertex in edge: glVertex3fv(vertices_cube[vertex])
    glEnd()

def draw_square(sh_x, sh_y, rx, ry):
    glBegin(GL_QUADS)
    for x, y, z in vertices_sq:
        # 1. Logika Refleksi
        nx = -x if ry else x
        ny = -y if rx else y
        # 2. Logika Shearing
        final_x = nx + sh_x * ny
        final_y = ny + sh_y * nx
        glVertex3f(final_x, final_y, z)
    glEnd()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    gluPerspective(45, (800 / 600), 0.1, 50.0)

    # State
    c_pos = [-2.5, 0, -10]; c_rot = 0
    s_pos = [2.5, 0, -10]
    s_sx = 0.0; s_sy = 0.0
    ref_x = False; ref_y = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            
            if event.type == KEYDOWN:
                # KONTROL KUBUS (W, S, A, D)
                if event.key == K_w: c_pos[1] += 0.2
                if event.key == K_s: c_pos[1] -= 0.2
                if event.key == K_a: c_rot -= 10
                if event.key == K_d: c_rot += 10

                # KONTROL PERSEGI (DIPERBAIKI)
                if event.key == K_UP: s_pos[1] += 0.2      # GERAK ATAS (Translasi)
                if event.key == K_DOWN: s_pos[1] -= 0.2    # GERAK BAWAH (Translasi)
                if event.key == K_LEFT: s_sx -= 0.1       # MIRING SAMPING (Shearing X)
                if event.key == K_RIGHT: s_sx += 0.1
                if event.key == K_r: s_sy += 0.1          # MIRING ATAS (Shearing Y)
                if event.key == K_t: s_sy -= 0.1
                if event.key == K_x: ref_x = not ref_x    # BALIK (Refleksi)
                if event.key == K_y: ref_y = not ref_y
                
                if event.key == K_SPACE: # RESET
                    s_sx = s_sy = 0.0; ref_x = ref_y = False; c_rot = 0; s_pos = [2.5, 0, -10]

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_DEPTH_TEST)

        # Kubus Merah
        glPushMatrix()
        glTranslatef(*c_pos)
        glRotatef(c_rot, 0, 1, 0)
        glColor3f(1.0, 0.0, 0.0)
        draw_cube()
        glPopMatrix()

        # Persegi Hijau
        glPushMatrix()
        glTranslatef(*s_pos)
        glColor3f(0.0, 1.0, 0.0)
        draw_square(s_sx, s_sy, ref_x, ref_y)
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()