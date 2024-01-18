/**************** Paramètres de la MAP **************** */

let lat = 40.419222121886904;
let lon = -3.704355955123902;
let precision = 18.747;

var map = L.map('map').setView([lat, lon], 16);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 20,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);


/**************** Expériences **************** */


/**
 * Expérience Lilia à Madrid
 * 
 * Situation : Je pars en vacances à Madrid. Trouvez-moi un hôtel parmi ceux marqués qui soit :
 * Près d'une supérette
 * Pas dans une rue avec beaucoup de passage
 * Pas à côté d'un bar
 * Pas trop loin de 2 ou 3 restos
 * 
 */

let hotels_madrid = [[40.419222121886904, -3.704355955123902], [40.41945082791583, -3.703722953796387], [40.41851149462177, -3.701276779174805], [40.414108705526225, -3.702746629714966], [40.413504218482984, -3.7049353122711186], [40.41338985545855, -3.7010407447814946], [40.41638773622095, -3.698937892913819], [40.415930302560234, -3.699506521224976], [40.41713105928677, -3.7092268466949467], [40.41735977242411, -3.7084543704986577], [40.41464783803734, -3.708368539810181], [40.41776001854368, -3.7063300609588627], [40.418593176298415, -3.7073385715484624], [40.419687701197596, -3.7074565887451176], [40.416992197359775, -3.70514988899231], [40.41869936232981, -3.704549074172974], [40.41876470749658, -3.703980445861817], [40.41850332644866, -3.7012875080108647], [40.41726992092716, -3.7024891376495366], [40.41683699839633, -3.7017488479614262], [40.415513708484866, -3.7054610252380376], [40.415905797097786, -3.705246448516846], [40.41579143815505, -3.7048172950744633], [40.41540751742568, -3.703776597976685], [40.41519513480451, -3.703025579452515], [40.41558722527384, -3.701877593994141], [40.4162161989626, -3.701781034469605]]

/**
 * Fonction qui ajoute les marqueurs associées aux hôtels tirés aléatoirement dans la liste hotels_madrid.
 * 
 * liste : liste totale avec coord de chaque hotel
 * lim : nombre d'hôtels qui appareissent sur la carte
 */

function test(liste,lim){ 
  
  let len = liste.length;
  let list_pts = [];
  for (i=0 ; i<len ; i++){
    list_pts.push(liste[i]);
  }

  while (list_pts.length>lim){
    let n = Math.random();
    let len = list_pts.length;
    let k = Math.round(n*(len-1));
    console.log('k=',k);
    list_pts.splice(k,1);
    console.log('len = ',list_pts.length);
  }

  for (let i=0; i<lim; i++){
    L.marker(list_pts[i]).addTo(map);
  }
}

test(hotels_madrid,6);


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

      map.on('dblclick click zoom dragstart dragend', onMapClick);
      map.on('mousemove', onMapClick);
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

        map.off('dblclick click zoom dragstart dragend', onMapClick);
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

  let ev = ['click', 'dblclick', 'zoom', 'dragstart', 'dragend'];

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

  dico['type'] = type;

  dico['temps'] = temps;
  dico['posLatLon'] = 'null';
  dico['posPix'] = 'null';
  dico['NOcorner'] = 'null';
  dico['center'] = 'null';
  dico['nivZoom'] = 'null';

  if (type == 'click' || type == 'dblclick' || type == 'mousemove'){
    dico['posLatLon'] = e.latlng;
    dico['posPix'] = e.containerPoint;
  }
  else{
    dico['NOcorner'] =  map.containerPointToLatLng(NOcorner);
    dico['center'] = map.containerPointToLatLng(center);
  
    if (type == 'zoom'){
      dico['nivZoom'] = map.getZoom();
    }
  }

  return dico;
}

function resetEventsColor(e){
  let events = ['click', 'dblclick', 'zoom', 'dragstart', 'dragend'];
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
