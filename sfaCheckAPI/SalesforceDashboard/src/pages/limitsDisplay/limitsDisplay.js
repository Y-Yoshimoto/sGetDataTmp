import React from "react";
import clsx from 'clsx';
//ダッシュボードテンプレート読み込み
import DashboardTemplate from "../../templates/Dashboard";
import { dsStyles, theme } from "../../templates/dsStyles";
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';
import Modal from '@material-ui/core/Modal';

//Recharts
import Meter from './Meter';
import HistoryChart from './HistoryChart';
//Nivo
import MeterNivo from './MeterNivo';

export default function LimitsDisplay() {
    // Paperのスタイルの設定
    const classes = dsStyles();
    const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);

    // メニュー表示切り替え
    const [open, setOpen] = React.useState(false);
    return (
        <DashboardTemplate title="使用状況ダッシュボード">
            <Grid container spacing={3} >
                <Grid item xs={12} md={6} lg={4}>
                    <Graph_PaperAndModal targetKey="DailyApiRequests" title="API使用履歴" ></Graph_PaperAndModal>
                </Grid>
                <Grid item xs={12} md={6} lg={4}>
                    <Graph_PaperAndModal targetKey="DataStorageMB" title="データ使用量(MB)" ></Graph_PaperAndModal>
                </Grid>
                <Grid item xs={12} md={6} lg={4}>
                    <Graph_PaperAndModal targetKey="FileStorageMB" title="ファイル使用量(MB)" ></Graph_PaperAndModal>
                </Grid>
                <Grid item xs={12} md={6} lg={4}>
                    <Paper className={fixedHeightPaper}>
                        <MeterNivo />
                    </Paper>
                </Grid>
            </Grid>
        </DashboardTemplate >
    )
};
//<Paper className={fixedHeightPaper}>

function Graph_PaperAndModal(props) {
    //ペーパースタイル
    const classes = dsStyles();
    const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);
    //モーダルスタイル読み込み
    const modalStyle = clsx(classes.modal);
    // モーダルの開閉制御
    const [ModalOpen, ModalOpenset] = React.useState(false);
    const handleOpen = () => {
        ModalOpenset(true);
    };
    const handleClose = () => {
        ModalOpenset(false);
    };

    return (
        <React.Fragment>
            <Paper className={fixedHeightPaper} onClick={handleOpen}>
                <Meter targetKey={props.targetKey} title={props.title} />
            </Paper>
            <Modal className={modalStyle} open={ModalOpen} onClose={handleClose}>
                <Paper className={fixedHeightPaper} onClick={handleOpen}>
                    <HistoryChart targetKey={props.targetKey} title={props.title} />
                </Paper>

            </Modal>
        </React.Fragment >
    );
}