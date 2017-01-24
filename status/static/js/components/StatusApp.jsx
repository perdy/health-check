import React from 'react';
import HealthApp from './HealthApp.jsx';
import StatsApp from './StatsApp.jsx';

/**
 * Retrieve the current TODO data from the StatusStore
 */
function getStatusState() {
  return {};
}

class StatusApp extends React.Component {
  render() {
    return (
      <div>
        <HealthApp/>
        <StatsApp/>
      </div>
    )
  }
}

StatusApp.propTypes = {};

StatusApp.defaultProps = {};

export default StatusApp;
