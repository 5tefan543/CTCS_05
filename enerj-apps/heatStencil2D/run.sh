 #!/bin/sh
enerjdir=../../enerj
mainclass=src/HeatStencil2D

enerjargs=-noisy

args=
for arg
do
    case "$arg" in
    -nonoise) enerjargs= ;;
    *) args="$args $arg" ;;
    esac
done

# Run HeatStencil2D
$enerjdir/bin/enerj -Xmx4096m $enerjargs $mainclass $args

# Output stats.
# $enerjdir/bin/enerjstats
