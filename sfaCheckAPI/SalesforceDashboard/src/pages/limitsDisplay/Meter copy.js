import React from 'react';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import { theme } from "./theme";

// グラフ用
// https://recharts.org/en-US
import {
    AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Text, Cell,
} from 'recharts';
import moment from 'moment';

let GETUSEINFOURI = 'http://127.0.0.1:8280/latestvalue/';
let MAXAPIUSERD = parseInt(15000);
let heightCharts = 400;

//グラフグリッド表示 
export class CharComponent extends React.Component {
    render() {
        return (
            <Grid container className={theme.root} spacing={1}>
                <Grid item lg={9} md={9} sm={12} xs={12} >
                    <Card ><CharCard value={"API使用履歴"} /><APIReqsInfoData /></Card>
                </Grid >
                <Grid item lg={3} md={3} sm={12} xs={12}>
                    <Card><CharCard value={"API平均使用量(直近1日)"} /><APIReqsInfoNow /></Card>
                </Grid>
            </Grid >
        )
    }
}
//表示用カードレンダリング
class Meter extends React.Component {
    render() {
        return (
            <CardContent>
                <Typography className={theme.title} color="textSecondary" gutterBottom>
                    {this.props.value}
                </Typography>
            </CardContent>
        )
    }
}

// UnixTimeからの変換
function sorttime(data) {
    data.sort((a, b) => a.time < b.time ? -1 : 1)
    return data
}

/****** 円グラフ表示　コンポーネント  ******/
// 表示ラベル
const label = ({ name, value, fill, cx, cy, midAngle, innerRadius, outerRadius, percent }) => {
    //数量パーセンテージ表
    const pielabel = String(value) + "(" + String((value / MAXAPIUSERD * 100.0).toFixed(2)) + "%)";
    //表示位置調整
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);
    return (
        <>
            <Text x={x} y={y} fill="black" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
                {name}
            </Text>
            <Text x={x} y={y + 18} dominantBaseline="hanging" fill="black" textAnchor={x > cx ? 'start' : 'end'}>{pielabel}</Text>

        </>
    )
}

class APIReqsInfoNow extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            APIReqsdata: []
        };
    }
    // 値取得
    componentDidMount() {
        const uri = GETUSEINFOURI + 'exportaverage/';
        fetch(uri)
            .then(response => response.json())
            .then(result => {
                this.setState({
                    isLoaded: true,
                    APIReqsdata: result
                });
                //console.log(result)
            })
            .catch(error => {
                this.setState({
                    isLoaded: true,
                    error
                });
                alert('Server Error.')
            })
    }
    render() {
        const COLORS = ['#FFA826', '#93D6A4']
        return (
            <ResponsiveContainer width="100%" height={heightCharts} onMouseEnter={this.onPieEnter}>
                <PieChart>
                    <Pie data={this.state.APIReqsdata} dataKey="value" label={label} labelLine={false} startAngle={180} endAngle={-180} minAngle={1}>
                        {
                            this.state.APIReqsdata.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />)
                        } </Pie>
                </PieChart>
            </ResponsiveContainer>
        );
    }
}