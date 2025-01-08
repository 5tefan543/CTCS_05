#!/bin/sh
enerjdir=../../enerj

args=-Alint=simulation,mbstatic
if [ "$1" = "-nosim" ]
then
enerjcargs="-Alint=mbstatic"
fi

$enerjdir/bin/enerjc $args HelloWorld.java
