Dieses Package beinhaltet verschiedene Nodes, die als Übungsaufgaben im WS24 gestellt wurden.
Im folgenden sind diese Nodes, ihre Funktionsweise und potentielle Parameter aufgelistet.

stopDrivingNode: Wenn die Node initialisiert wird, publisht sie einen Twist mit linear.x = angular.z = 0. Die Datei enthält außerdem die Funktion spinUntilKeyboardInterrupt, die eine andere Node spinnt und bei einem Keyboard-Interrupt die Stoproutine ausführt.

followObstacleNode: Der Roboter nutzt den Laserscanner, um dem nächsten Objekt in seinem Sichtfenster zu folgen.
    Parameter:
    - distance_to_slow_down: Distanz, ab der die langsame Geschwindigkeit genutzt wird
    - distance_to_stop: Distanz, an der der Roboter stehen bleibt
    - speed_slow: Schnelle Geschwindigkeit für entfernte Objekte
    - speed_fast: Langsame Geschwindigkeit für nahe Objekte
    - speed_slow_turn: Langsame Drehgeschwindigkeit, genutzt für Objekte die sich vor dem Roboter befinden
    - speed_fast_turn: Schnelle Drehgeschwindigkeit, genutzt für Objekte die sich hinter dem Roboter befinden
    - window: Fenster, in dem der Roboter Objekte beachtet, in 2*Grad (auf 180 setzen um alles zu beachten)
    - debug: Auf true setzen, um das versenden der Fahrbefehle auszuschalten

followLineNode: Der Roboter nutzt die Kamera, um einer Linie auf dem Boden zu folgen. Dabei wird nur die unterste Pixelzeile beachtet.
    Parameter:
    - boundary-left: Grenze links, ab der keine Linie mehr erkannt wird
    - boundary-right: Grenze rechts, ab der keine Linie mehr erkannt wird
    - speed_drive: Geschwindigkeit zum fahren
    - speed_turn: Geschwindigkeit zu drehen