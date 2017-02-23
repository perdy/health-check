import React from 'react';
import StatsStore from '../stores/StatsStore';
import StatsItem from './StatsItem.jsx';

class StatsApp extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      items: props.items,
      name: props.name
    };
    this._onChange = () => this.setState(() => { return {items: StatsStore.getAll()} });
  }

  componentDidMount() {
    StatsStore.addChangeListener(this._onChange);
  }

  componentWillUnmount() {
    StatsStore.removeChangeListener(this._onChange);
  }

  render() {
    var items = [];

    for (var name in this.state.items) {
      if (this.state.items.hasOwnProperty(name)) {
        items.push(
          <StatsItem key={name} name={name} status={this.state.items[name]}/>
        );
      }
    }

    return (
      <div className="row">
        <div className="col-xs-12">
          { items }
        </div>
      </div>
    )
  }
}

StatsApp.propTypes = {
  items: React.PropTypes.object.isRequired,
  name: React.PropTypes.string
};

StatsApp.defaultProps = {
  items: {},
  name: "Stats"
};

export default StatsApp;
