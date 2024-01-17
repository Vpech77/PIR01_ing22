/**************** Paramètres de la MAP **************** */

let lat = 48.8408075;
let lon = 2.5873473;
let precision = 18.747;

let latUni = 55.87171291246245;
let lonUni = -4.288390874862672;

var map = L.map('map').setView([latUni, lonUni], 14);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let hotels = [[55.87519572537305, -4.282361268997193, 51], [55.87502870194355, -4.277440756559373, 98],
              [55.87740119485359, -4.2874494194984445, 98], [55.866066314876235, -4.285773038864137, 80],
              [55.86433394514431, -4.265313148498536, 86], [55.86419095722301, -4.258457422256471, 71]];

for (let i=0; i<hotels.length; i++){
  let markers = L.marker([hotels[i][0], hotels[i][1]]).addTo(map);
  markers.bindPopup("<b>Hôtel</b><br>Nuit : "+hotels[i][2]+"€").openPopup();
}

var marker = L.marker([latUni, lonUni]).addTo(map);
    
var circle = L.circle([latUni, lonUni], {
    color: 'red',
    fillColor: '#f03',
    fillOpacity: 0.5,
    radius: precision,
}).addTo(map);

marker.bindPopup("<b>Here your conference</b><br>University of Glasgow").openPopup();


/**************** tracker  **************** */

let track = Vue.createApp({
  data() {
    return {
      nom:"session0",
      lstEvents: [],
      nbEvents: 0,

      dataEvents: [],
      dataMouseEvents:[],

      starttime: 0,
      time: {
        minutes: 0,
        secondes: 0,
        milisec: 0
      },
      etat: {
        run: true,
        stop: false
      },
    };
  },
  methods: {
    start () {
      this.startTime = Date.now();

      map.on('dblclick click zoom dragstart dragend zoomstart zoomend movestart move moveend', onMapClick);
      map.on('mousemove', onMapClick);
      //map.on('move', e => console.log(e))
      document.getElementById("map").addEventListener("wheel", detectTrackPad, true);
      
      /*document.getElementById("map").addEventListener("wheel", function(){
        console.log("L'événement wheel a été déclenché");
        });
      */

      if (this.etat.run){
        chronoStart();
        this.etat.run = false;
      }
      else{
        chronoStop();
        let csvContent = dicoToFormatCSV(this.dataEvents);
        dataToCSV(csvContent, "allEvents");
        let csvContentMouse = dicoToFormatCSV(this.dataMouseEvents);
        dataToCSV(csvContentMouse, "mouseMoveEvents");

        map.off('dblclick click zoom dragstart dragend movestart moveend zoomstart zoomend', onMapClick);
        map.off('mousemove', onMapClick);
        document.getElementById("map").removeEventListener("wheel", detectTrackPad, false);
        
        this.dataEvents = [];
        this.dataMouseEvents = [];
        this.nbEvents = 0;
        this.lstEvents = [];
      }
    },

  },

}).mount('#tracker');


/**************** chrono  **************** */

function onMapClick(e) {

  let ev = ['click', 'dblclick', 'zoom', 'dragstart', 'dragend', 'movestart', 'move', 'moveend', 'zoomstart', 'zoomend'];

  let dicoTemps = {
              min:track.time.minutes,
              sec:track.time.secondes,
              mili:track.time.milisec
              };

  let temps = JSON.stringify(dicoTemps);

  if (ev.includes(e.type)){
    resetEventsColor(e.type);
    track.nbEvents++;
    track.lstEvents.push(e);
    return track.dataEvents.push(createDicoEvent(e, temps));
  }

  if (e.type == 'mousemove'){
    return track.dataMouseEvents.push(createDicoEvent(e, temps));
  }
}

function createDicoEvent(e, temps){

  let dico = {};
  let type = e.type;
  let NOcorner = L.point(0,0);
  let center = L.point(250,250);
  let trans = e.target._mapPane._leaflet_pos

  dico['type'] = type;

  if (type=='zoomstart'){
    console.log("---------------------------------------");
  }

  dico['temps'] = temps;
  dico['posLatLon'] = 'null';
  dico['posPix'] = 'null';
  dico['NOcorner'] = 'null';
  dico['center'] = 'null';
  dico['nivZoom'] = 'null';
  dico['trans'] = 'null';

  if (type == 'click' || type == 'dblclick' || type == 'mousemove'){
    dico['posLatLon'] = e.latlng;
    dico['posPix'] = e.containerPoint;
  }
  else{
    dico['NOcorner'] =  map.containerPointToLatLng(NOcorner);
    dico['center'] = map.containerPointToLatLng(center);
    dico['trans'] = trans;
  
    if (type == 'zoom' || type == 'zoomstart' || type == 'zoomend'){
      dico['nivZoom'] = map.getZoom();
      console.log(type," : ", map.getZoom());
    }
  }

  return dico;
}

function resetEventsColor(e){
  let events = ['click', 'dblclick', 'zoom', 'dragstart', 'dragend', 'movestart', 'move', 'moveend', 'zoomstart', 'zoomend'];

  for (ev of events){
    document.getElementById(ev).classList.remove('rouge');
  }
  
  document.getElementById(e).classList.add('rouge');

}


/**************** chrono  **************** */
let timer;

chronoStart = function() {
  timer = setInterval(function() {
    let now = Date.now();
    let diff = new Date(now-track.startTime)
    track.time.minutes = diff.getMinutes();
    track.time.secondes = diff.getSeconds();
    track.time.milisec = diff.getMilliseconds();
  }, 100);
  setEtat(false, true);
};

chronoStop = function() {
  clearInterval(timer);
  setEtat(true, false);
};

setEtat = function(run, stop) {
  track.etat.run = run;
  track.etat.stop = stop;     
};

/**************** detect trackpad **************** */
let oldTime = 0;
let newTime = 0;
let isTrackPad;
let eventCount = 0;
let eventCountStart;

function detectTrackPad(e) {
  let isTrackPadDefined = isTrackPad || typeof isTrackPad !== "undefined";
  
  if (isTrackPadDefined) return;
  
  if (eventCount === 0) {
    eventCountStart = performance.now();
  }

  eventCount++;

  if (performance.now() - eventCountStart > 66) {
    if (eventCount > 6) {
      isTrackPad = true;
      console.log("Using trackpad");
      track.dataEvents.push(["Using trackpad"]);
    } else {
      isTrackPad = false;
      console.log("Using mouse");
      track.dataEvents.push(["Using mouse"]);
    }
    isTrackPadDefined = true;
  }
};
