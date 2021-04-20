import Link from '@material-ui/core/Link';
import Typography from '@material-ui/core/Typography';

// コピーライト
export default function Copyright() {
    return (
        <Typography variant="body2" color="textSecondary" align="center">
            {'hoges.co.jp © '}
            <Link color="inherit" href="https://hoges.co.jp/AdministratorDashboard">
                hoges.co.jp
      </Link>{' '}
            {new Date().getFullYear()}
            {'.'}
        </Typography>
    );
}