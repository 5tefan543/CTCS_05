#!/bin/sh
enerjdir=../../enerj

enerjargs=-noisy
if [ "$1" = "-nonoise" ]
then
enerjargs=
fi

$enerjdir/bin/enerj $enerjargs src/Mandelbrot