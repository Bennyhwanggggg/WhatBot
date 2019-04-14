import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { getBarchartData, get3DData, getPiechartData, getTimelineData } from '../actions';
import { connect } from 'react-redux'
import uuid from 'uuid';
import './stylesheets/Dashboard.css';
import 'echarts-gl/dist/echarts-gl';

class Dashboard extends React.Component {

    componentDidMount() {
        this.props.getBarchartData();
        this.props.get3DData();
        this.props.getPiechartData();
        this.props.getTimelineData();
    }

    state = {
        active: "Usage",
        currentGraph: this.props.piechart
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
                            style={{height: '700px', width: '100%'}}
                        />
                    </div>
                )
            })
        )
    }

    render() {
        const { active } = this.state;
        return (
            <div className="Dashboard">
                <div className="ui grid dashboard-grid">
                    <div className="four wide column">
                        <div className="ui vertical fluid tabular menu vertical-menu">
                            <a className={ active == "Usage" ? "active item" : "item" } onClick={() => this.setState({currentGraph: this.props.piechart, active: "Usage"})}>
                                Usage
                            </a>
                            <a className={ active == "Timeline" ? "active item" : "item" } onClick={() => this.setState({currentGraph: this.props.timeline, active: "Timeline"})}>
                                Activities Timeline
                            </a>
                            <a className={ active == "Activity" ? "active item" : "item" } onClick={() => this.setState({currentGraph: this.props.threeD, active: "Activity"})}>
                                Usage Activity
                            </a>
                            <a className={ active == "Quality" ? "active item" : "item" } onClick={() => this.setState({currentGraph: this.props.barchart, active: "Quality"})}>
                                Quality Control
                            </a>
                        </div>
                    </div>
                    <div className="twelve wide stretched column">
                        <div className="ui segment">
                            {this.generateChart(this.state.currentGraph)}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

const mapStateToProps = (state) => {
    return {piechart: Object.values(state.dashboard.piechart),
            timeline: Object.values(state.dashboard.timeline),
            threeD: Object.values(state.dashboard.threeD),
            barchart: Object.values(state.dashboard.barchart) }
}

export default connect(
    mapStateToProps,
    { getBarchartData, get3DData, getPiechartData, getTimelineData }
)(Dashboard);