
1 Erstelle ein mikroskopisch simuliertes Verkehrsszenario bestehend aus
a. einer zweispurigen Straße (ca. 2 km, ohne Lichtsignalanlage am Ende),
b. einem Abzweig auf ca. halber Strecke, der zu einem Ladepunkt (Charging Station) und von dort wieder zurück auf die zweispurige Straße führt,
c. einem Fahrzeugtyp (bspw. PKW) mit repräsentativer Parametrierung des Energiebedarfsmodells (nutze das SUMO Electric Modell unter https://sumo.dlr.de/docs/Models/Electric.html, nicht HBEFA),
d. einem Verkehrsfluss mit Fahrzeugen (200 Fzg./h), die mit einem zufälligen Ladezustand instanziiert werden (Simulationsdauer 1 h).
2. Im Regelfall fahren Fahrzeuge entlang der zweispurigen Straße. Falls jedoch der Ladezustand eines Fahrzeugs vor dem Abzweig unter eine (sinnvoll gewählte) Schwelle fällt, erhält das Fahrzeug eine neue Route, die es zur Ladestelle führt, wo das Fahrzeug (1.) hält und (2.) geladen wird bis der Ladezustand eine (sinnvoll gewählte) Schwelle wieder überschreitet. Anschließend fährt das Fahrzeug weiter. Es sollen mehrere Fahrzeuge gleichzeitig geladen werden können. Haltende bzw. ladende Fahrzeuge sollen nachfolgende nach Möglichkeit nicht blockieren.
3. Wähle eine sinnvolle Leistung für die Energieübertragung am Ladepunkt. Werte die gesamte Energiebilanz (über alle Fahrzeuge) aus. Erstelle ein Histogramm über die Energiebilanz aller Fahrzeuge.
