import AppDispatcher from '../dispatcher/AppDispatcher';
import AppConstants from '../constants/AppConstants';

var AppActions = {

  /**
   * Update a single Health check
   * @param {string} url The url of Health checks api view
   * @param {string} name The name of the Health check item
   */
  updateHealth: function(url, name) {
    AppDispatcher.handleAction({
      actionType: AppConstants.HEALTH_UPDATE,
      url: url,
      name: name
    });
  },

  /**
   * Update all items from health app.
   * @param {string} url The url of Health checks api view
   */
  updateHealthAll: function(url) {
    AppDispatcher.handleAction({
      actionType: AppConstants.HEALTH_UPDATE_ALL,
      url: url
    });
  },

  /**
   * Update a single Stats
   * @param {string} url The url of Stats api view
   * @param {string} name The name of the Stats item
   */
  updateStats: function(url, name) {
    AppDispatcher.handleAction({
      actionType: AppConstants.STATS_UPDATE,
      url: url,
      id: name
    });
  },

  /**
   * Update all items from stats app.
   * @param {string} url The url of Stats api view
   */
  updateStatsAll: function(url) {
    AppDispatcher.handleAction({
      actionType: AppConstants.STATS_UPDATE_ALL,
      url: url
    });
  },
};

export default AppActions;
