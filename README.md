Dieses Repository entsteht als Übung für ROS2, welches im Rahmen des Moduls Robotikprojekt im Wintersemester 24/25 an der TU Berakademie Freiberg verwendet wird.

Das Package timing_tubaf_cpp stellt eine einfache Publisher-Node namens "talker" bereit, der sekündlich eine Nachricht verschickt.
Das Listener-Komplement "listener" dazu findet sich in timing_tubaf_py.
Beide Packages enthalten außerdem eine Beispiel-Node namens "example_node", die einen Hello-World ähnlichen String in zurückgibt.

Bevor die Packages gebaut werden können, muss erst in der Root "rosdep install -i --from-path src --rosdistro humble -y" ausgeführt werden.
Der Befehl zum bauen ist "colcon build", mit dem Parameter "--packages-select [PACKAGENAME]" können Packages einzeln gebaut werden.

Zum Ausführen der Nodes muss ein neues Terminal in der Root geöffnet werden, dann mit "source install/setup.bash" die Setup-Dateien gesourct und schlussendlich "ros2 run [PACKAGENAME] [NODENAME]" ausgeführt werden.