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
        <div id="downloadCSV"></div>
        </div>


        <div id="map"></div>
    </div>



    <div id="menu">
        <form action="" @submit.prevent="hello">
            <label>Votre nom : <input type="text" v-model="nom"></label>
            <button class="btn btn-primary" @click="hello">ok</button>
        </form>

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
                    <li >keyboard</li>
                    <li>mouse</li>
                    <li>trackpad</li>
                    <li>touch</li>
                </ul>

            </ul>
        </div>


        <h2>Menu</h2>
        <h3>Liens principaux</h3>
        <ul>
            <li><a href="https://ensg_dei.gitlab.io/web-az/webmapping/vs-intro/">Cours de ProgWeb</a></li>
            <li><a href="https://leafletjs.com/reference.html">Doc Leaflet</a></li>
        </ul>
        <h3>Raccourci</h3>
        <ul>
            <li><a href="https://ensg_dei.gitlab.io/web-az/js/dom/">Events + Vue</a></li>
            <li><a href="https://leafletjs.com/reference.html#map-event">Map events Leaflet</a></li>
            <li><a href="https://leafletjs.com/reference.html#map-methods-for-getting-map-state">Get state map</a></li>
        </ul>

    </div>



    <div id="footer"></div>
    
    <script src="https://cdn.jsdelivr.net/npm/vue"></script>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
        integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
        crossorigin=""></script>
    <script src="../assets/js/createCSV.js"></script>
    <script src="../assets/js/map.js"></script>
</body>
</html>