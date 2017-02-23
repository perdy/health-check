import $ from 'jquery';
import events from "events";
import assign from "object-assign";
import AppDispatcher from "../dispatcher/AppDispatcher";
import AppConstants from "../constants/AppConstants";

var EventEmitter = events.EventEmitter;

var CHANGE_EVENT = 'change';

var _health_check = {
  health: {},
  stats: {}
};

/**
 * Create a HealthCheck item.
 * @param {string} name The name of the HealthCheck
 * @param {string} content The content of the HealthCheck
 */
function create(type, name, content) {
  // Using the current timestamp + random number in place of a real id.
  _health_check[name] = {
    name: name,
    status: content
  };
}

/**
 * Update a HealthCheck item.
 * @param {string} name The name of the HealthCheck
 * @param {object} updates An object literal containing only the data to be
 *     updated.
 */
function update(name, updates) {
  _health_check[name] = assign({}, _health_check[name], updates);
}

/**
 * Delete a HealthCheck item.
 * @param {string} name The name of the HealthCheck
 */
function destroy(name) {
  delete _health_check[name];
}

var HealthCheckStore = assign({}, EventEmitter.prototype, {
  /**
   * Get the entire collection of TODOs.
   * @return {object}
   */
  getAll: function () {
    return _health_check;
  },

  emitChange: function () {
    this.emit(CHANGE_EVENT);
  },

  /**
   * @param {function} callback
   */
  addChangeListener: function (callback) {
    this.on(CHANGE_EVENT, callback);
  },

  /**
   * @param {function} callback
   */
  removeChangeListener: function (callback) {
    this.removeListener(CHANGE_EVENT, callback);
  }
});

// Register callback to handle all updates
AppDispatcher.register(function (action) {
  switch (action.actionType) {
    case AppConstants.HEALTH_CHECK_UPDATE_ALL:
      $.get('/health_check/api')
        .done((data) => {
          _health_check = data;
          HealthCheckStore.emitChange();
        });
      break;

    default:
    // no op
  }
});

export default HealthCheckStore;
