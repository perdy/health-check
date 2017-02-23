import $ from 'jquery';
import 'bootstrap';

import React from "react";
import ReactDOM from "react-dom";
import HealthCheckApp from "./components/HealthCheckApp.jsx";
import AppActions from "./actions/AppActions";

ReactDOM.render(
  <HealthCheckApp />,
  document.getElementById('app')
);

const update = (urls) => {
  AppActions.updateHealthAll(urls['health']);
  AppActions.updateStatsAll(urls['stats']);
}

$(document).ready(() => {
  var api_urls = {
    health: $('#health_url').html(),
    stats: $('#stats_url').html()
  }

  update(api_urls);
  setInterval(() => { update(api_urls) }, 60000);
});
