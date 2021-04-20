const express = require('express');
var moment = require("moment");
function timeFormatJ(time) {
    datehour = moment(time).format("M/D H");
    return datehour + "時"
}
function timeFormatU(time) {
    return (moment(time).unix());
}

// ヒストリーデータ取得
module.exports = function (receiveFromAppJs) {
    var router = express.Router();
    const InfluxdbConnection = require("./InfluxdbConnection");
    const InConnecter = new InfluxdbConnection()

    // 履歴値取得API
    router.get('/:key', (req, res) => {
        const data = InConnecter.getItems(req.params.key, req.query.field)
            .then(result =>
                res.send(result)
            )
    });


    // 折れ線グラフ用履歴値取得API
    router.get('/AreaChartdata/:key', (req, res) => {
        const data = InConnecter.getItems(req.params.key, req.query.field)
            .then(result => {
                //const lists = result.map(function (x) { return { "key": x.key, "time": x.time, "field": x._field, "value": x._value } })
                //console.log(lists)
                res.send(result.map(function (x) { return { "key": x.key, "time": x._time.slice(0, -9), "unixtime": timeFormatU(x._time), "field": x._field, "value": x._value } }))
            })
    });
    return router;
}

