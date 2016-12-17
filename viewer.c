#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include <time.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#if defined(__APPLE__)
#include <OpenGL/gl.h>
#include <GLUT/glut.h>
#else
#include <GL/gl.h>
#include <GL/glut.h>
#endif
#include "fract.h"

static const int K = 8;
static int render_pts = 16;
static int show_grid = 1;
static struct fract *fract;

static void reshape_callback(int width, int height)
{
	glViewport(0, 0, width, height);
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();

	glDisable(GL_BLEND);
	glDisable(GL_DEPTH_TEST);
	glDisable(GL_LIGHTING);
	glDisable(GL_CULL_FACE);
	glDisable(GL_TEXTURE_2D);
	glEnable(GL_LINE_SMOOTH);
	glEnable(GL_POINT_SMOOTH);
}

static void display_callback()
{
	glClearColor(1.0f, 1.0f, 1.0f, 0.0f);
	glClear(GL_COLOR_BUFFER_BIT);

	if (show_grid) {
		int render_k = (int) ceil(log((double) render_pts) / log(2.0));
		int bucket_width_k = (int) ceil(render_k / 2.0);

		glLineWidth(1.5f);
		glBegin(GL_LINES);

		for (int i = 0; i < (1 << render_k); ++i) {
			if (i % (1 << bucket_width_k) == 0)
				glColor3f(0.5f, 0.5f, 1.0f);
			else
				glColor3f(0.5f, 0.5f, 0.5f);
			float a = (float) i / (1 << render_k);
			glVertex2f(0.0f, a);
			glVertex2f(1.0f, a);
			glVertex2f(a, 0.0f);
			glVertex2f(a, 1.0f);
		}
		glEnd();
	}

	glPointSize(10.0f);
	glColor3f(0.0f, 0.0f, 0.0f);
	glBegin(GL_POINTS);
	for (int i = 0; i < render_pts; ++i) {
		float u, v;
		fract_get(fract, 0, i, &u, &v);
		glVertex2f(u, v);
	}
	glEnd();

	glutSwapBuffers();
}

static void keyboard_callback(unsigned char key, int x, int y)
{
	switch (key) {
	case ' ':
		if (render_pts < (1 << K))
			++render_pts;
		printf("render_pts: %d\n", render_pts);
		break;
	case 127:
	case '\b':
		if (render_pts > 0)
			--render_pts;
		printf("render_pts: %d\n", render_pts);
		break;
	case 'g':
		show_grid = !show_grid;
		break;
	case 'r':
		if (fract)
			fract_free(fract);
		fract = fract_init(1);
		break;
	case 'q':
		exit(0);
	}
	glutPostRedisplay();
}

int main(int argc, char **argv)
{
	srand(time(NULL));

	fract = fract_init(1);

	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(720, 720);
	glutCreateWindow("fract");

	glutReshapeFunc(reshape_callback);
	glutDisplayFunc(display_callback);
	glutKeyboardFunc(keyboard_callback);

	glutMainLoop();

	fract_free(fract);

	return 0;
}
