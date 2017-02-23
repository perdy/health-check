import React from 'react';

class HealthItem extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      name: props.name,
      status: props.status
    };
  }

  healthy() {
    var result = true;
    var check = this.props.status;

    for (var i in check) {
      if (result && check.hasOwnProperty(i) && check[i] === false) {
        result = false;
      }
    }

    return result;
  }

  /**
   * @return {object}
   */
  render() {
    var name = this.props.name;
    var rendered;
    if (this.healthy()) {
      rendered = (
        <li className="list-group-item">
          <span className="pull-xs-right">
            <i className="fa fa-check text-success" aria-hidden="true"></i>
          </span>
          <span className="text-capitalize">{ name }</span>
        </li>
      )
    } else {
      rendered = (
        <li className="list-group-item">
          <span className="pull-xs-right">
            <i className="fa fa-close text-danger" aria-hidden="true"></i>
          </span>
          <span className="text-capitalize">{ name }</span>
        </li>
      )
    }
    return rendered;
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
