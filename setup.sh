python runCozy.py -i setup.cz > /dev/null 2>&1 &

PID=$(ps -ef | grep "setup.cz" | awk {'print$2'})
PID=$(echo $PID | awk {'print $1'})
sleep 0.9

kill $PID 2>/dev/null
wait $PID 2>/dev/null


echo "Setup Complete"
