import * as React from 'react';
import clsx from 'clsx';
import CssBaseline from '@material-ui/core/CssBaseline';
import Drawer from '@material-ui/core/Drawer';
import Box from '@material-ui/core/Box';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import List from '@material-ui/core/List';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import IconButton from '@material-ui/core/IconButton';
import Badge from '@material-ui/core/Badge';
import Container from '@material-ui/core/Container';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import Link from '@material-ui/core/Link';
import MenuIcon from '@material-ui/icons/Menu';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import NotificationsIcon from '@material-ui/icons/Notifications';
import ClickAwayListener from '@material-ui/core/ClickAwayListener';


// 　ダッシュボードスタイルインポート
import { dsStyles, theme } from './dsStyles';

// メニューリスト
import { mainListItems, secondaryListItems } from './listItems';

// モジュールインポート
import Copyright from './module/Copyright';

//export default function Dashboard() {
export default function DashboardTemplate(props) {
  const classes = dsStyles();
  // メニュー表示切り替え
  const [open, setOpen] = React.useState(false);
  const toggleDrawer = () => {
    setOpen(!open);
  };
  const fixedHeightPaper = clsx(classes.paper, classes.fixedHeight);
  // 画面表示 -------------------------------------------------------------------------
  return (
    <div className={classes.root}>
      <CssBaseline />
      <AppBar
        theme={theme}
        position="absolute"
        className={clsx(classes.appBar, open && classes.appBarShift)}
      >
        {/* ツールバー --------------------------------------------------------------*/}
        <Toolbar
          className={classes.toolbar}>
          {/* メニューボタン  ClickAwayListener外部コンポーネントのクリック検知*/}
          {/* <ClickAwayListener onClickAway={toggleDrawer}> */}
          <IconButton
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={toggleDrawer}>
            <MenuIcon />
          </IconButton>
          {/* </ClickAwayListener> */}
          {/* タイトル */}
          <Typography
            component="h1"
            variant="h6"
            color="inherit"
            noWrap
            className={classes.title}          >
            {props.title}
          </Typography>
          {/* 通知アイコン */}
          <IconButton color="inherit">
            <Badge badgeContent={0} color="secondary">
              <NotificationsIcon />
            </Badge>
          </IconButton>

        </Toolbar>
      </AppBar>

      { /* メニュー    --------------------------------------------------------------*/}
      <Drawer
        classes={{
          paper: clsx(classes.drawerPaper, !open && classes.drawerPaperClose),
        }}
        open={open}>{/*常時表示時追加 variant="permanent" */}

        {/* 閉じるボタン */}
        <div className={classes.toolbarIcon}>
          <IconButton onClick={toggleDrawer}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider />
        <List>{mainListItems}</List>
        <Divider />
        <List>{secondaryListItems}</List>
      </Drawer>

      {/*ダッシュボード メインボード --------------------------------------------------*/}
      <main className={classes.content}>
        <div className={classes.appBarSpacer} />
        <Container maxWidth="xl" className={classes.container}>
          {/* メインコンテンツ */}
          {props.children}
          {/* コピーライト */}
          <Box sx={{ pt: 4 }}>
            <Copyright />
          </Box>
        </Container>
      </main>
    </div >
  );
}
