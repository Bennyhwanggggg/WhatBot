import React from 'react';
import ReactEcharts from 'echarts-for-react';
import { getDashboardData } from '../actions';
import { connect } from 'react-redux'
import './stylesheets/Dashboard.css';
import uuid from 'uuid';

class Dashboard extends React.Component {

    componentDidMount() {
        this.props.getDashboardData();
    }

    generateChart = () => {
        if (this.props.piechart.length === 0) {
            return (
                <div className="loading-screen">
                    <div className="ui active centered inline loader"></div>
                </div>
            )
        }
        return (
            this.props.piechart.map(chart => {
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
                <div class="ui grid charts">
                    <div class="fifteen wide column">
                        {this.generateChart()}
                    </div>
                    <div class="fifteen wide column">
                        {this.generateChart()}
                    </div>
                    <div class="fifteen wide column">
                        {this.generateChart()}
                    </div>
                    <div class="fifteen wide column">
                        {this.generateChart()}
                    </div>
                </div>
            </div>
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