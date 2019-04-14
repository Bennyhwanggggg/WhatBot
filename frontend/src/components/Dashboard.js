import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { getBarchartData, get3DData, getPiechartData, getTimelineData } from '../actions';
import { connect } from 'react-redux'
import uuid from 'uuid';
import './stylesheets/Dashboard.css';
import 'echarts-gl/dist/echarts-gl';

class Dashboard extends React.Component {

    state = {
        active: "Usage",
        currentGraphName: "piechart",
        currentGraphData: this.props.piechart
    }

    componentDidMount() {
        this.props.getBarchartData();
        this.props.get3DData();
        this.props.getPiechartData();
        this.props.getTimelineData();
    }

    componentDidUpdate() {
        if (this.state.currentGraphName === 'piechart' && this.state.currentGraphData !== this.props.piechart) {
            this.setState({ active: "Usage",
                            currentGraphName: 'piechart',
                            currentGraphData: this.props.piechart})
        }
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
                    <div className="three wide column">
                        <div className="ui vertical fluid tabular menu vertical-menu">
                            <div className={ active === "Usage" ? "active item" : "item" } onClick={() => this.setState({currentGraphData: this.props.piechart, currentGraphName: 'piechart', active: "Usage"})}>
                                Usage
                            </div>
                            <div className={ active === "Timeline" ? "active item" : "item" } onClick={() => this.setState({currentGraphData: this.props.timeline, currentGraphName: 'timeline', active: "Timeline"})}>
                                Activities Timeline
                            </div>
                            <div className={ active === "Activity" ? "active item" : "item" } onClick={() => this.setState({currentGraphData: this.props.threeD, currentGraphName: 'threeD', active: "Activity"})}>
                                Usage Activity
                            </div>
                            <div className={ active === "Quality" ? "active item" : "item" } onClick={() => this.setState({currentGraphData: this.props.barchart, currentGraphName: 'barchart', active: "Quality"})}>
                                Quality Control
                            </div>
                        </div>
                    </div>
                    <div className="thirteen wide stretched column">
                        <div className="ui segment">
                            {this.generateChart(this.state.currentGraphData)}
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