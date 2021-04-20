import React from 'react';
import { useTheme } from '@material-ui/core/styles';

// install (please make sure versions match peerDependencies)
// yarn add @nivo/core @nivo/pie
import { ResponsivePie } from '@nivo/pie'

// make sure parent container have a defined height when using
// responsive component, otherwise height will be 0 and
// no chart will be rendered.
// website examples showcase many properties,
// you'll often use just a few of them.
var datas = [
    {
        "id": "php",
        "label": "php",
        "value": 568,
        "color": "hsl(77, 70%, 50%)"
    },
    {
        "id": "c",
        "label": "c",
        "value": 457,
        "color": "hsl(56, 70%, 50%)"
    }]
export default function MeterNivo(props) {
    return (
        "test"
    )
}