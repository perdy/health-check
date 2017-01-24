import React from 'react';
import StatsStore from "../stores/StatsStore";

class StatsItemKey extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      statsChainKeys: props.statsChainKeys,
      status: props.status
    };

    this.toggleArrow = this.toggleArrow.bind(this);

    this._onChange = () => this.setState(() => {
      var stats = StatsStore.get(this.state.statsChainKeys[0]);

      for (var key in this.state.statsChainKeys.slice(1)) {
        stats = stats[key];
      }

      return {status: stats}
    });
  }

  getChainID() {
    var capitalizeIDs = this.state.statsChainKeys.slice(1).map((value) => {
      return value[0].toUpperCase() + value.slice(1);
    });

    return this.state.statsChainKeys[0] + capitalizeIDs.join('');
  }

  name() {
    return this.state.statsChainKeys[this.state.statsChainKeys.length - 1];
  }

  toggleArrow() {
    this.refs.arrow.classList.toggle('fa-rotate-90');
  }

  render() {
    var result = null;

    var id = this.getChainID();

    if (typeof this.state.status === 'object' && this.state.status instanceof Array) {
      // Check if array
      items = [];

      for (var item in this.state.status) {
        if (this.state.status.hasOwnProperty(item)) {
          items.push(<a href="#" className="list-group-item">{ this.state.status[item] }</a>)
        }
      }

      result = (
        <div>
          <a href={'#' + id} className="list-group-item" data-toggle="collapse" ref="collapsable">
            <i className="fa fa-chevron-right fa-rotate-90" aria-hidden="true"/>
            { this.name() }
          </a>
          <div className="list-group collapse in" id={ id }>
            { items }
          </div>
        </div>
      )
    } else if (this.state.status && Object.keys(this.state.status).length > 0
      && this.state.status.constructor === Object) { // Isn't empty
      // Check if object
      var items = [];
      var i = 0;

      for (var item in this.state.status) {
        if (this.state.status.hasOwnProperty(item)) {
          var statsChainKey = this.state.statsChainKeys.slice();
          statsChainKey.push(item);
          items.push(
            <StatsItemKey key={statsChainKey} status={this.state.status[item]} statsChainKeys={statsChainKey}/>
          )
        }
      }

      result = (
        <div className="nested-node">
          <a href={'#' + id} className="list-group-item" data-toggle="collapse" onClick={ this.toggleArrow }>
            <i className="fa fa-chevron-right fa-rotate-90" aria-hidden="true" ref="arrow"/>
            { this.name() }
          </a>
          <div className="list-group collapse in" id={ id }>
            { items }
          </div>
        </div>
      )
    } else {
      // Simple element
      item = this.state.status;
      if (typeof item !== "undefined" && item && item.constructor !== Object) {
        var value = item.toString();
      } else {
        value = ""
      }

      result = (
        <a href="#" className="list-group-item nested-leaf">
          <span>{ this.name() }</span>
          <span className="pull-right">{ value }</span>
        </a>
      )
    }

    return result;
  }
}

StatsItemKey.propTypes = {
  statsChainKeys: React.PropTypes.arrayOf(React.PropTypes.string).isRequired,
  status: React.PropTypes.any
};

StatsItemKey.defaultProps = {
  statsChainKeys: [],
  status: {}
};

export default StatsItemKey;
