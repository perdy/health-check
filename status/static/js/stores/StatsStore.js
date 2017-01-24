import $ from 'jquery';
import events from "events";
import assign from "object-assign";
import AppDispatcher from "../dispatcher/AppDispatcher";
import AppConstants from "../constants/AppConstants";

var EventEmitter = events.EventEmitter;

var CHANGE_EVENT = 'change';

var _stats = {};


/**
 * Create an item.
 * @param {string} name The name of the Stats
 * @param {string} content The content of the Stats
 */
function create(name, content) {
  _stats[name] = {
    name: name,
    status: content
  };
}

/**
 * Update an item.
 * @param {string} name The name of the Stats
 * @param {object} updates An object literal containing only the data to be
 *     updated.
 */
function update(name, updates) {
  _stats[name] = assign({}, _stats[name], updates);
}

/**
 * Delete an item.
 * @param {string} name The name of the Stats
 */
function destroy(name) {
  delete _stats[name];
}
/**
 * Update a single item.
 * @param {string} url Url to query for data
 * @param {string} name Health check name
 */
function updateSingle(url, name) {
  $.get(url)
    .done((data) => {
      if (data.hasOwnProperty(name)) {
        update(name, data[name])
      }
      StatsStore.emitChange();
    });
}

/**
 * Update all items.
 * @param {string} url Url to query for data
 */
function updateAll(url) {
  $.get(url)
    .done((data) => {
      for (var item in data) {
        if (data.hasOwnProperty(item)) {
          update(item, data[item])
        }
      }
      StatsStore.emitChange();
    });
}

var StatsStore = assign({}, EventEmitter.prototype, {
  /**
   * Get the entire collection.
   * @return {object}
   */
  getAll: function () {
    return _stats;
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
    case AppConstants.STATS_UPDATE_ALL:
      updateAll(action.url);
      break;

    case AppConstants.STATS_UPDATE:
      updateSingle(action.url, action.name);
      break;

    default:
    // no op
  }
});

export default StatsStore;
