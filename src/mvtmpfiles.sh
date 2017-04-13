#!/usr/bin/csh
set local_forcingdir = $1
echo $local_forcingdir

echo $local_forcingdir/Rainf_regional/tmp 
mv $local_forcingdir\/Rainf_regional/tmp/* $local_forcingdir\/Rainf_regional

echo done
