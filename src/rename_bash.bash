bash-4.2$ j=1
bash-4.2$ for i in Gridbox\ rainfall\ rate200*.png; do
> new=$(printf "a-%04d.png" "$j")
> mv -- "$i" "$new"
> let j=j+1
> done

for i in Gridbox\ moisture\ content\ of\ each\ soil\ layer2008_*.png; do new=$(printf "b-%04d.png" "$j"); mv -- "$i" "$new"; let j=j+1; done
