import React from 'react';
import { useTheme } from '@material-ui/core/styles';
//import Grid from '@material-ui/core/Grid';
//import Card from '@material-ui/core/Card';
//import CardContent from '@material-ui/core/CardContent';
//import Typography from '@material-ui/core/Typography';
// import { theme } from "./theme";

import { Title, Subtitle } from './Title';

// グラフ用
// https://recharts.org/en-US
import {
    ResponsiveContainer, PieChart, Pie, Text, Cell,
} from 'recharts';
//import moment from 'moment';

let GETUSEINFOURI = 'http://127.0.0.1:8280/limitinfo/latestvalue/PieChartdata/';

export default function Meter(props) {
    const theme = useTheme();
    //console.log(props.targetKey)
    //console.log(props.title)
    return (
        <React.Fragment>
            {/*<Title>{props.title}</Title>*/}
            <Title>{props.title}</Title>
            <ResponsiveContainer width="100%" height="100%" >
                <APIReqsInfoNow targetKey={props.targetKey} />
            </ResponsiveContainer>
        </React.Fragment>
    );
}

//const data = [
//    { name: 'Group A', value: 400 }, { name: 'Group B', value: 300 }
//];
// 表示ラベル
const renderCustomizedLabel = ({ label, value, fill, cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    //数量パーセンテージ表
    //const pielabel = String(value) + "(" + String((value / MAXAPIUSERD * 100.0).toFixed(2)) + "%)";
    //表示位置調整
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);
    return (
        <>
            <Text x={x} y={y - 15} fill="black" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
                {label}
            </Text>
            <Text x={x} y={y - 8} dominantBaseline="hanging" fill="black" textAnchor={x > cx ? 'start' : 'end'}>{value}</Text>
        </>
    )
}

//最新値ベースの円グラフを表示
class APIReqsInfoNow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            APIReqsdata: []
        };
    }
    // API経由で値取得
    componentDidMount(props) {
        const uri = GETUSEINFOURI + this.props.targetKey;
        //console.log(uri)
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
    // グラフ描画描画
    render() {
        const COLORS = ['#FFA826', '#93D6A4']
        return (
            <React.Fragment><Subtitle>{this.state.APIReqsdata.UsageRate + "%"}</Subtitle>
                <PieChart width={300} height={300} margin={{
                    top: 0, right: 0, bottom: 0, left: 50
                }} onMouseEnter={this.onPieEnter}>
                    <Pie
                        data={this.state.APIReqsdata.data}
                        dataKey="value"
                        label={renderCustomizedLabel}
                        labelLine={false}
                        startAngle={180}
                        endAngle={-180}
                        minAngle={1}
                        outerRadius={"100%"}>
                        {
                            [0, 1].map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
                        }</Pie>
                </PieChart >
            </React.Fragment>
        );
    }
}
