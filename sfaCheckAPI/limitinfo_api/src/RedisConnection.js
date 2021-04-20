const redis = require('ioredis')

// 接続情報
const config = {
    host: 'redis_c',
    port: 6379
}

class RedisConnection {
    constructor() {
        // 接続
        this.client = new redis(config)
        console.log("RedisConnection")
    }
    // 値登録
    set(key, value) {
        this.client.set(key, value)
    }
    // 値取得
    get(key) {
        return this.client.get(key)
            .then(function (result) {
                return result
            });
    }
    // データセット登録
    setItems(key, body) {
        this.client.set(key + "_Max", body.Max)
        this.client.set(key + "_Using", body.Using)
        this.client.set(key + "_UsageRate", body.UsageRate)
        this.client.set(key + "_Remaining", body.Remaining)
    }
    // データセット取得
    async getItems(key) {
        const Max = await this.client.get(key + "_Max")
        const Using = await this.client.get(key + "_Using")
        const UsageRate = await this.client.get(key + "_UsageRate")
        const Remaining = await this.client.get(key + "_Remaining")
        const result = { "Item": key, "Max": Max, "Using": Using, "UsageRate": UsageRate, "Remaining": Remaining }
        return result
    }

}
module.exports = RedisConnection;