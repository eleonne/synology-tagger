import React from "react";
import ReactApexChart from "react-apexcharts";
import { getChartOptions, getChartData, secondsToDhms } from '../../assets/utils'
import axios from "axios";

class LineChart extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      chartData: [],
      chartOptions: {},
    };
  }

  componentDidMount() {
    this.setState({
      chartData: this.props.chartData,
      chartOptions: this.props.chartOptions,
    });
  }

  componentDidUpdate() {
    // console.log('chart update')
  }

  loadAgain(values, labels) {
    this.setState({
      chartData: values,
      chartOptions: labels,
    });
  }

  render() {
    return (
      <ReactApexChart
        options={this.state.chartOptions}
        series={this.state.chartData}
        type='line'
        width='100%'
        height='100%'
      />
    );
  }
}

export default LineChart;
