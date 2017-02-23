import React from 'react';
import HealthStore from '../stores/HealthStore';
import HealthItem from './HealthItem.jsx';

/**
 * Retrieve the current TODO data from the StatusStore
 */
function getState() {
  return {
    items: HealthStore.getAll()
  };
}

class HealthApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      items: props.items,
      name: props.name
    };
    this._onChange = () => this.setState(() => { return {items: HealthStore.getAll()} });
  }

  componentDidMount() {
    HealthStore.addChangeListener(this._onChange);
  }

  componentWillUnmount() {
    HealthStore.removeChangeListener(this._onChange);
  }

  render() {
    var items = [];

    for (var name in this.state.items) {
      if (this.state.items.hasOwnProperty(name)) {
        items.push(
          <HealthItem key={name} name={name} status={this.state.items[name]}/>
        );
      }
    }

    return (
      <div className="row">
        <div className="col-xs-12">
          <div className="card">
            <div className="card-block">
              <h4 className="card-title">{ this.state.name }</h4>
            </div>
            <div className="card-block">
              <ul className="list-group list-group-flush">{ items }</ul>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

HealthApp.propTypes = {
  items: React.PropTypes.object.isRequired,
  name: React.PropTypes.string
};

HealthApp.defaultProps = {
  items: {},
  name: "Health Check"
};

export default HealthApp;
