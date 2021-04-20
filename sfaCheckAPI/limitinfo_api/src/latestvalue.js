const express = require('express');


// 最新値取得API
module.exports = function (receiveFromAppJs) {
    var router = express.Router();
    // Redis接続 関数読み込み
    const RedisConnection = require("./RedisConnection");
    const RConnecter = new RedisConnection()

    // 最新値取得API
    router.get('/:key', (req, res) => {
        const data = RConnecter.getItems(req.params.key)
            .then(result =>
                res.send(result)
            )
    });

    // 円グラフ表示用値取得API
    router.get('/PieChartdata/:key', (req, res) => {
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
    router.post('/:key', (req, res) => {
        // console.log(req.body.Item)
        if (process.env.ACCESS_KEY == req.header('Access_key')) {
            RConnecter.setItems(req.params.key, req.body)
            res.send('200');
        } else {
            res.send('401');
        }
    });

    return router;
}