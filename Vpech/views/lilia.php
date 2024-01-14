<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
    crossorigin=""/>

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="../assets/css/accueil.css">

    <title>Vcookie</title>
</head>
<body>


    <div id="entete">
        <h1>LOST IN Guillaume Touya PIR</h1>
    </div>

    <div id="contenu">

        <div id="tracker">
        <button id="startbutton" class="btn btn-primary" @click="start">Start tracking</button>
        <div id="timer">{{time.minutes}} minutes et {{time.secondes}} secondes</div>
        <div id="downloadCSV">
            <div id="allEvents"></div>
            <div id="mouseMoveEvents"></div>
        </div>
        </div>


        <div id="map"></div>
    </div>



    <div id="menu">

        <div id="events">
            <h2>Events</h2>
            <ul>
                <li id="click">click</li>
                <li id="dblclick">dblclick</li>
                <li id="mousemove">mousemove</li>
                <li id="dragstart">dragstart</li>
                <li id="dragend">dragend</li>
            </ul>
            <ul>
                
                <li id="zoom">zoom</li>
                <ul>
                    <li>keyboard</li>
                    <li>mouse</li>
                    <li>trackpad</li>
                    <li>touch</li>
                </ul>

            </ul>
        </div>


        <h2>Menu</h2>
        <h3>Situation</h3>
        <p>Je pars en vacances à Madrid. Trouvez-moi un hôtel parmi ceux marqués qui soit :</p>
            <p>- Près d'une supérette</p>
            <p>- Pas dans une rue avec beaucoup de passage</p>
            <p>- Pas à côté d'un bar</p>
            <p>- Pas trop loin de 2 ou 3 restos</p>

        <h3>Expériences</h3>
        <ul>
            <li><a href="/">Expérience Vanessa</a></li>
        </ul>

    </div>



    <div id="footer"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/vue"></script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>
    <script src="../assets/js/createCSV.js"></script>
    <script src="../assets/js/mapLilia.js"></script>
</body>
</html>