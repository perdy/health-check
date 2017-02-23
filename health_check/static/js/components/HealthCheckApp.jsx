import React from 'react';
import HealthApp from './HealthApp.jsx';
import StatsApp from './StatsApp.jsx';

/**
 * Retrieve the current TODO data from the StatusStore
 */
class HealthCheckApp extends React.Component {
  render() {
    return (
      <div>
        <HealthApp/>
        <StatsApp/>
      </div>
    )
  }
}

HealthCheckApp.propTypes = {};

HealthCheckApp.defaultProps = {};

export default HealthCheckApp;
