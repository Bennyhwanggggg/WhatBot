import React from 'react';
import ReactEcharts from 'echarts-for-react'; 

class Dashboard extends React.Component {

    sample_chart_option = () => {
        
    }

    generateChart = () => {
        return (
            <ReactEcharts
                option={this.getOption()}
                notMerge={true}
                lazyUpdate={true}
                theme={"theme_name"}
                onChartReady={this.onChartReadyCallback}
                onEvents={EventsDict}
                opts={} />
        )
    }

    render() {
        return (
            <div>{this.generateChart()}</div>
        )
    }
}

export default Dashboard;