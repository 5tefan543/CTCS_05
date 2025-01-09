#!/bin/sh
enerjdir=../../enerj

enerjargs=-noisy
if [ "$1" = "-nonoise" ]
then
enerjargs=
fi

$enerjdir/bin/enerj -Xmx10240m $enerjargs src/Mandelbrot 160 80 true