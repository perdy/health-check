import $ from 'jquery';
import events from "events";
import assign from "object-assign";
import AppDispatcher from "../dispatcher/AppDispatcher";
import AppConstants from "../constants/AppConstants";

var EventEmitter = events.EventEmitter;

var CHANGE_EVENT = 'change';

var _status = {
  health: {},
  stats: {}
};

/**
 * Create a Status item.
 * @param {string} name The name of the Status
 * @param {string} content The content of the Status
 */
function create(type, name, content) {
  // Using the current timestamp + random number in place of a real id.
  _status[name] = {
    name: name,
    status: content
  };
}

/**
 * Update a Status item.
 * @param {string} name The name of the Status
 * @param {object} updates An object literal containing only the data to be
 *     updated.
 */
function update(name, updates) {
  _status[name] = assign({}, _status[name], updates);
}

/**
 * Delete a Status item.
 * @param {string} name The name of the Status
 */
function destroy(name) {
  delete _status[name];
}

var StatusStore = assign({}, EventEmitter.prototype, {
  /**
   * Get the entire collection of TODOs.
   * @return {object}
   */
  getAll: function () {
    return _status;
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
    case AppConstants.STATUS_UPDATE_ALL:
      $.get('/status/api')
        .done((data) => {
          _status = data;
          StatusStore.emitChange();
        });
      break;

    default:
    // no op
  }
});

export default StatusStore;
