#!/bin/sh
enerjdir=../../enerj
mainclass=HelloWorld

enerjargs=-noisy
if [ "$1" = "-nonoise" ]
then
enerjargs=
fi

# Run HelloWorld.
$enerjdir/bin/enerj $enerjargs $mainclass

# Output stats.
# $enerjdir/bin/enerjstats
