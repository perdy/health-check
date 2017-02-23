import $ from 'jquery';
import events from "events";
import assign from "object-assign";
import AppDispatcher from "../dispatcher/AppDispatcher";
import AppConstants from "../constants/AppConstants";

var EventEmitter = events.EventEmitter;

var CHANGE_EVENT = 'change';

var _health = {};

/**
 * Create an item.
 * @param {string} name The name of the Health check
 * @param {string} content The content of the Health check
 */
function create(name, content) {
  _health[name] = {
    name: name,
    status: content
  };
}

/**
 * Update an item.
 * @param {string} name The name of the Health check
 * @param {object} updates An object literal containing only the data to be
 *     updated.
 */
function update(name, updates) {
  _health[name] = assign({}, _health[name], updates);
}

/**
 * Delete an item.
 * @param {string} name The name of the Health check
 */
function destroy(name) {
  delete _health[name];
}

/**
 * Update a single Health check.
 * @param url Url to query for data
 * @param name Health check name
 */
function updateSingle(url, name) {
  $.get(url)
    .done((data) => {
      if (data.hasOwnProperty(name)) {
        update(name, data[name])
      }
      HealthStore.emitChange();
    });
}

/**
 * Update all Health checks.
 * @param url Url to query for data
 */
function updateAll(url) {
  $.get(url)
    .done((data) => {
      for (var item in data) {
        if (data.hasOwnProperty(item)) {
          update(item, data[item])
        }
      }
      HealthStore.emitChange();
    });
}

var HealthStore = assign({}, EventEmitter.prototype, {
  /**
   * Get a single element.
   * @param name
   * @returns {object}
   */
  get: function (name) {
    return _health[name];
  },

  /**
   * Get the entire collection.
   * @return {object}
   */
  getAll: function () {
    return _health;
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
AppDispatcher.register(function (payload) {
  var action = payload.action;

  switch (action.actionType) {
    case AppConstants.HEALTH_UPDATE_ALL:
      updateAll(action.url);
      break;

    case AppConstants.HEALTH_UPDATE:
      updateSingle(action.url, action.name);
      break;

    default:
    // no op
  }
});

export default HealthStore;
