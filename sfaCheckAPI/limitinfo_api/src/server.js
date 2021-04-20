'use strict';
// express,bodyParser読み込み
// https://expressjs.com/ja/guide/routing.html
const express = require('express');
const bodyParser = require('body-parser');

// express起動
const PORT = 8040;
const HOST = '0.0.0.0';
const app = express();

// urlencoded,jsonパース
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json());

//
app.get('/healthCheck', function (req, res) {
    res.send("OK")
});


//LatestValue 最新値API Redis取得
app.use('/latestvalue', require('./latestvalue.js')());
//HistoryValue 履歴値API InfluxDB取得
app.use('/historyvalue', require('./historyvalue.js')());

// サーバ起動
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);