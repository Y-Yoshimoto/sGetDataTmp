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

// アプリケーション
// 関数読み込み
const RedisConnection = require("./RedisConnection");
const RConnecter = new RedisConnection()
// 取得API
app.get('/:key', (req, res) => {
    const data = RConnecter.getItems(req.params.key)
        .then(result =>
            res.send(result)
        )
});
// 円グラフ表示用
app.get('/PieChartdata/:key', (req, res) => {
    const data = RConnecter.getItems(req.params.key)
        .then(data => {
            const result = {
                "targetKey": req.params.key,
                "UsageRate": Number(data["UsageRate"]).toFixed(2),
                "data": [{
                    "id": "Using",
                    "value": Number(data["Using"]),
                    "label": "使用"
                }, {
                    "id": "Remaining",
                    "value": Number(data["Remaining"]),
                    "label": "未使用"
                }]
            }
            //console.log(result)
            res.send(result)
        })
});



// 登録API
app.post('/:key', (req, res) => {
    // console.log(req.body.Item)
    if (process.env.ACCESS_KEY == req.header('Access_key')) {
        RConnecter.setItems(req.params.key, req.body)
        res.send('200');
    } else {
        res.send('401');
    }

});
// サーバ起動
app.listen(PORT, HOST);
console.log(`Running on http://${HOST}:${PORT}`);