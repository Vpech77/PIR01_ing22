<?php

require 'flight/Flight.php';

Flight::route('/', function () {
    Flight::render('accueil');

});

Flight::route('/lilia', function () {
    Flight::render('lilia');

});

Flight::start();

?>