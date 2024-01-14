<?php

require 'flight/Flight.php';

Flight::route('/', function () {
    Flight::render('accueil');

});

Flight::route('/lilia', function () {
    Flight::render('lilia');

});

Flight::route('/proto', function () {
    Flight::render('proto');

});

Flight::route('/test', function () {
    Flight::render('test');

});

Flight::start();

?>