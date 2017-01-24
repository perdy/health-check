import React from 'react';
import HealthStore from "../stores/HealthStore";

class HealthItem extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: props.name,
      status: props.status
    };
    this._onChange = () => this.setState(() => { return {status: HealthStore.get(this.state.name)} });
  }

  healthy() {
    var result = true;
    var status = this.state.status;

    for (var i in status) {
      if (result && status.hasOwnProperty(i) && status[i] === false) {
        result = false;
      }
    }

    return result;
  }

  /**
   * @return {object}
   */
  render() {
    var healthy = this.healthy();

    return (
      <li className="list-group-item">
        <span className="pull-xs-right">
          <i className={healthy ? "fa fa-check text-success" : "fa fa-close text-danger"} aria-hidden="true"/>
        </span>
        <span className="text-capitalize">{ this.state.name }</span>
      </li>
    )
  }
}

HealthItem.propTypes = {
  name: React.PropTypes.string.isRequired,
  status: React.PropTypes.object.isRequired
};

HealthItem.defaultProps = {
  name: '',
  status: {}
};

export default HealthItem;
