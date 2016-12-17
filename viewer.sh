#!/bin/bash

LIBS="-lm  -lGL -lglut"
if [[ "$OSTYPE" == "darwin"* ]]; then
    LIBS="-lm -framework GLUT -framework OpenGL"
fi

cc -std=c99 -Wall -O2 fract.c viewer.c -o viewer $LIBS && ./viewer
