import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";


import topPage from "./pages/topPage/topPage";
import limitsDisplay from "./pages/limitsDisplay/limitsDisplay";
import Dashboard from "./officialTemplate/Dashboard";

//import { theme } from "./theme";

class SfaDataAggregater extends React.Component {
    render() {
        return (
            <Router>
                <Switch>
                    <Route path="/" component={topPage} exact />
                    <Route path="/limitsDisplay" component={limitsDisplay} exact />
                    <Route path="/dashboard" component={Dashboard} exact />
                </Switch>
            </Router>
        )
    }
}

ReactDOM.render(
    <SfaDataAggregater />,
    document.getElementById('root')
);