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
        return (
            <div className="Dashboard">
                <div class="ui grid dashboard-grid">
                    <div class="four wide column">
                        <div class="ui vertical fluid tabular menu vertical-menu">
                            <a class="active item">
                                Bio
                            </a>
                            <a class="item">
                                Pics
                            </a>
                            <a class="item">
                                Companies
                            </a>
                            <a class="item">
                                Links
                            </a>
                        </div>
                    </div>
                    <div class="twelve wide stretched column">
                        <div class="ui segment">
                        This is an stretched grid column. This segment will always match the tab height
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