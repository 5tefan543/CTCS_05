#!/bin/sh
enerjdir=../../enerj

args=-Alint=simulation
if [ "$1" = "-nosim" ]
then
args=
fi

$enerjdir/bin/enerjc $args src/HeatStencil2D.java
