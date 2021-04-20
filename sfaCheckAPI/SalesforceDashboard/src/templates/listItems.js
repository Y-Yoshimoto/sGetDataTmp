import * as React from 'react';
import { Link } from "react-router-dom";
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';



// Icons Linlk
// https://material-ui.com/components/material-icons/
import DashboardIcon from '@material-ui/icons/Dashboard';
import AssessmentIcon from '@material-ui/icons/Assessment';

// 　ダッシュボードスタイルインポート
import { dsStyles, theme } from './dsStyles';

//メインメニューリスト
export const mainListItems = (
  <div theme={theme}>
    <LinkListItemPrimary title="トップページ" link="/">
      <DashboardIcon />
    </LinkListItemPrimary>
  </div>
);
//サブメニューリスト
export const secondaryListItems = (
  <div theme={theme}>
    <ListSubheader inset>サブメニュー</ListSubheader>
    <LinkListItemSecondary title="使用状況" link="/limitsDisplay">
      <AssessmentIcon />
    </LinkListItemSecondary>
  </div>
);


//メインメニュー表示
function LinkListItemPrimary(props) {
  const classes = dsStyles();
  return (
    <Link to={props.link} className={classes.link}>
      <ListItem button>
        <ListItemIcon>
          {props.children}
        </ListItemIcon>
        <ListItemText primary={props.title} />
      </ListItem>
    </Link>
  )
}

//サブメニュー表示
function LinkListItemSecondary(props) {
  const classes = dsStyles();
  return (
    <Link to={props.link} className={classes.link}>
      <ListItem button>
        <ListItemIcon>
          {props.children}
        </ListItemIcon>
        <ListItemText secondary={props.title} />
      </ListItem>
    </Link>
  )
}