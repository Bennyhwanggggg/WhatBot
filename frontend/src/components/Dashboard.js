import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { getBarchartData, get3DData, getPiechartData, getTimelineData } from '../actions';
import { connect } from 'react-redux'
import './stylesheets/Dashboard.css';
import uuid from 'uuid';

class Dashboard extends React.Component {

    componentDidMount() {
        this.props.getBarchartData();
        this.props.get3DData();
        this.props.getPiechartData();
        this.props.getTimelineData();
    }

    generateChart = (chartData) => {
        if (chartData.length === 0) {
            return (
                <div className="loading-screen">
                    <div className="ui active centered inline loader"></div>
                </div>
            )
        }
        return (
            chartData.map(chart => {
                return (
                    <div className="chart" key={uuid.v4()}>
                        <ReactEcharts
                            option={chart}
                        />
                    </div>
                )
            })
        )
    }

    render() {
        return (
            <div className="Dashboard">
                <div className="ui grid charts">
                    <div className="fifteen wide column">
                        {this.generateChart(this.props.piechart)}
                    </div>
                    <div className="fifteen wide column">
                        {this.generateChart(this.props.timeline)}
                    </div>
                    <div className="fifteen wide column">
                        {this.generateChart(this.props.threeD)}
                    </div>
                    <div className="fifteen wide column">
                        {this.generateChart(this.props.barchart)}
                    </div>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    console.log(state)
    return {piechart: Object.values(state.dashboard.piechart),
            timeline: Object.values(state.dashboard.timeline),
            threeD: Object.values(state.dashboard.threeD),
            barchart: Object.values(state.dashboard.barchart) }
}

export default connect(
    mapStateToProps,
    { getBarchartData, get3DData, getPiechartData, getTimelineData }
)(Dashboard);