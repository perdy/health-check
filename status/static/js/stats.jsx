import $ from 'jquery';
import 'bootstrap';

import React from "react";
import ReactDOM from "react-dom";
import StatsApp from "./components/StatsApp.jsx";
import AppActions from "./actions/AppActions";

ReactDOM.render(
  <StatsApp />,
  document.getElementById('app')
);

$(document).ready(() => {
  var api_url = $('#api_url').html();
  AppActions.updateStatsAll(api_url);
  setInterval(() => { AppActions.updateStatsAll(api_url) }, 60000);
});
