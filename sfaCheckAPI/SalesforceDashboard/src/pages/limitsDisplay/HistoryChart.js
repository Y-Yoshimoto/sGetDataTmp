import React from 'react';
import { useTheme } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

import { Title, Subtitle } from './Title';

// グラフ用
// https://recharts.org/en-US
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Text, Cell,
} from 'recharts';
import moment from 'moment';

let GETUSEINFOURI = 'http://127.0.0.1:8280/limitinfo/historyvalue/AreaChartdata/'
//let DATAFIELD = '?field=UsageRate'
let DATAFIELD = '?field=Using'
let MAXAPIUSERD = parseInt(15000);
let heightCharts = 400;

export default function HistoryChart(props) {
    const theme = useTheme();
    //console.log(props.targetKey)
    //console.log(props.title)
    return (
        <React.Fragment>
            {/*<Title>{props.title}</Title>*/}
            <Title>{props.title}</Title>
            <ResponsiveContainer width="100%" height="100%" >
                <APIReqsInfoData targetKey={props.targetKey} />
            </ResponsiveContainer>
        </React.Fragment>
    );
}

//const data = [
//    {"key":"DailyApiRequests","time":"2021-04-04T16:17:48.7747478Z","field":"UsageRate","value":0.16},
//    { "key": "DailyApiRequests", "time": "2021-04-04T16:17:51.295436Z", "field": "UsageRate", "value": 0.16 },
//    { "key": "DailyApiRequests", "time": "2021-04-04T16:18:27.4632588Z", "field": "UsageRate", "value": 0.16666666666666666 },
//    { "key": "DailyApiRequests", "time": "2021-04-04T16:20:18.2494719Z", "field": "UsageRate", "value": 0.22 },
//    { "key": "DailyApiRequests", "time": "2021-04-04T16:32:44.6213141Z", "field": "UsageRate", "value": 0.22666666666666666 },
//    { "key": "DailyApiRequests", "time": "2021-04-04T16:43:27.5789543Z", "field": "UsageRate", "value": 0.23333333333333334 },
//    { "key": "DailyApiRequests", "time": "2021-04-05T14:06:08.9098097Z", "field": "UsageRate", "value": 0.12 }
//];
/****** 面グラフ表示　コンポーネント  ******/
class APIReqsInfoData extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            APIReqsdata: []
        };
    }
    // 値取得
    componentDidMount(props) {
        const uri = GETUSEINFOURI + this.props.targetKey + DATAFIELD;
        console.log(uri)
        fetch(uri)
            .then(response => response.json())
            .then(result => {
                this.setState({
                    isLoaded: true,
                    APIReqsdata: result
                });
                console.log(result)
            })
            .catch(error => {
                this.setState({
                    isLoaded: true,
                    error
                });
                alert('Server Error.')
            })
    }
    // レンダリング
    render() {
        return (
            <React.Fragment>
                <AreaChart
                    width={1200}
                    height={500}
                    data={this.state.APIReqsdata}
                    margin={{
                        top: 0, right: 20, left: 20, bottom: 0,
                    }}>
                    <defs>
                        <linearGradient id="colorGr" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="50%" stopColor="#007EB1" stopOpacity={0.8} />
                            <stop offset="100%" stopColor="#007EB1" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis
                        dataKey="unixtime"
                        tickFormatter={(unixtime) => moment(unixtime, "X").format("M/D H") + "時"}
                        domain={["dataMin", "dataMax"]}
                        type='number'
                    />
                    <YAxis label={{ value: "使用回数", angle: -90, offset: -5, position: "insideLeft" }} />
                    <Tooltip
                        dataKey="unixtime"
                        labelFormatter={(unixtime) => moment(unixtime, "X").format("M/D HH:mm:ss")}
                    />
                    <Area type="monotone" dataKey="value" name="使用回数" legendType="none" stroke="#064583" fill="url(#colorGr)" />
                </AreaChart>
            </React.Fragment>
        );
    }
}
//                        tickFormatter={(unixTime) => moment(unixTime, "X").format("M/D H") + "時"}
//                        
//                        domain={["dataMin", "dataMax"]}
//                          type = 'number'