const { InfluxDB, FluxTableMetaData } = require('@influxdata/influxdb-client')

const config = {
    url: process.env['INFLUX_URL'] || 'http://influxdb_c:8086',
    token: process.env['INFLUX_TOKEN'] || 'wJmvpkBMrn0OTtcWtxQJylBPqIo7H931GJ5xl917aJ9mBJxW4PmWC6LUk-twLorSbfjLZomMukXiIuBFtEdCgw==',
    org: process.env['INFLUX_ORG'] || 'SfaTimebaseMetrics',
    bucket: 'SfaTimebaseMetrics',
    username: 'SfaTimebaseMetrics',
    password: 'Password01'
};

class InfluxdbConnection {
    constructor() {
        const url = 'http://influxdb_c:8086';
        const token = 'wJmvpkBMrn0OTtcWtxQJylBPqIo7H931GJ5xl917aJ9mBJxW4PmWC6LUk-twLorSbfjLZomMukXiIuBFtEdCgw==';
        this.client = new InfluxDB({ url, token })
        this.queryApi = this.client.getQueryApi('SfaTimebaseMetrics')
        //this.fluxQuery =
        //'from(bucket: "SfaTimebaseMetrics") |> range(start: -336h)|> filter(fn: (r) => r._measurement == "LimitProcessing" and r.key == "DailyApiRequests" and r._field == "Using")'
        console.log("InfluxdbConnection")
    }
    //クエリー作成
    makefluxQuery(range, measurement, key, field) {
        let fluxQuery = 'from(bucket: "SfaTimebaseMetrics") ';
        fluxQuery += ('|> range(start: -' + String(range) + 'h) ')
        fluxQuery += ('|> filter(fn: (r) => r._measurement == "' + String(measurement) + '" and ')
        fluxQuery += ('r.key == "' + String(key) + '" and r._field == "' + String(field) + '")')
        console.log(fluxQuery)
        return fluxQuery
    }

    //値取得
    getdate(fluxQuery) {
        return this.queryApi.collectRows(fluxQuery)
            .then(data => {
                //console.log("Get Success")
                //data.forEach(x => console.log(JSON.stringify(x)))
                //console.log('\nCollect ROWS SUCCESS')
                return data
            })
            .catch(error => {
                //console.log("Get Error")
                console.error(error)
                console.log('\nQueryRaw ERROR')
                return error
            })
    }

    async getItems(key, field) {
        //const result = { "Item": key, "Max": "100" }
        const fluxQuery = this.makefluxQuery(336, "LimitProcessing", key, field)
        const result = await this.getdate(fluxQuery)
        return result
    }
}
module.exports = InfluxdbConnection;