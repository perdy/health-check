import $ from 'jquery';
import 'bootstrap';

import React from "react";
import ReactDOM from "react-dom";
import HealthApp from "./components/HealthApp.jsx";
import AppActions from "./actions/AppActions";

ReactDOM.render(
  <HealthApp />,
  document.getElementById('app')
);

$(document).ready(() => {
  var api_url = $('#api_url').html();
  AppActions.updateHealthAll(api_url);
  setInterval(() => { AppActions.updateHealthAll(api_url) }, 60000);
});
