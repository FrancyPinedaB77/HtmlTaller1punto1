
onINT() {
echo "Killing command1 $command1PID too"
kill -KILL "$command1PID"
exit
}

trap "onINT" SIGINT
python grab.py &
command1PID="$!"
python manage.py runserver 0.0.0.0:8080
echo Done


