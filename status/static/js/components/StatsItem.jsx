import React from 'react';
import StatsStore from "../stores/StatsStore";
import StatsItemKey from "./StatsItemKey.jsx";

class StatsItem extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      name: props.name,
      status: props.status
    };

    this._onChange = () => this.setState(() => {
      return {status: StatsStore.get(this.state.name)}
    });
  }

  /**
   * @return {object}
   */
  render() {
    var objects = [];

    for (var item in this.state.status) {
      if (this.state.status.hasOwnProperty(item)) {
        var key = this.state.name + item[0].toUpperCase() + item.slice(1);
        objects.push(
          <StatsItemKey key={ key } statsChainKeys={ [this.state.name, item] } status={ this.state.status[item] }/>
        )
      }
    }

    return (
      <div className="card">
        <div className="card-block">
          <h4 className="card-title">{ this.state.name }</h4>
        </div>
        <div className="card-block">
          <div className="nested-list-group">
            <div className="list-group well">
              { objects }
            </div>
          </div>
        </div>
      </div>
    );
  }
}

StatsItem.propTypes = {
  name: React.PropTypes.string.isRequired,
  status: React.PropTypes.object.isRequired
};

StatsItem.defaultProps = {
  name: '',
  status: {}
};

export default StatsItem;
