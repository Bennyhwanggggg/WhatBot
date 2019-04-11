import React from 'react';
import ReactEcharts from 'echarts-for-react'; 

class Dashboard extends React.Component {

    sample_chart_option = () => {
        var option = {
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b}: {c} ({d}%)"
            },
            legend: {
                orient: "vertical",
                x: "left",
                data:["cconsultation_booking","prerequisites_queries","indicative_hours_queries","course_outline_queries","course_location_queries"]
            },
            series: [
                {
                    name:"intents",
                    type:"pie",
                    radius: ["50%", "70%"],
                    avoidLabelOverlap: false,
                    label: {
                        normal: {
                            show: false,
                            position: "center"
                        },
                        emphasis: {
                            show: true,
                            textStyle: {
                                fontSize: "30",
                                fontWeight: "bold"
                            }
                        }
                    },
                    labelLine: {
                        normal: {
                            show: false
                        }
                    },
                    data:[
                        {value:335, name:"consultation_booking"},
                        {value:310, name:"prerequisites_queries"},
                        {value:234, name:"indicative_hours_queries"},
                        {value:1135, name:"course_outline_queries"},
                        {value:1548, name:"course_location_queries"}
                    ]
                }
            ]
         };
         return option;
    }

    generateChart = () => {
        return (
            <ReactEcharts
                option={this.sample_chart_option()}
                 />
        )
    }

    render() {
        return (
            <div className="Dashboard">{this.generateChart()}</div>
        )
    }
}

export default Dashboard;