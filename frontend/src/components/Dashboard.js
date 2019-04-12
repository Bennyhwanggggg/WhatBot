import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { getDashboardData } from '../actions';
import { connect } from 'react-redux'
import './stylesheets/Dashboard.css';

class Dashboard extends React.Component {

    componentDidMount() {
        this.props.getDashboardData();
    }

    generateChart = () => {
        console.log(this.props.piechart)
        if (this.props.piechart.length === 0) {
            return (
                <div className="loading-screen">
                    <div className="ui active centered inline loader"></div>
                </div>
            )
        }
        return (
            <ReactEcharts
                option={this.props.piechart}
                 />
        )
    }

    render() {
        return (
            <div className="Dashboard">{this.generateChart()}</div>
        )
    }
}

const mapStateToProps = (state) => {
    console.log(state)
    return {piechart: Object.values(state.dashboard.piechart) }
}

export default connect(
    mapStateToProps,
    { getDashboardData }
)(Dashboard);