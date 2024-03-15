import { Paper, Typography } from '@mui/material';
import Backdrop from '@mui/material/Backdrop/Backdrop';
import CircularProgress from '@mui/material/CircularProgress/CircularProgress';
import PropTypes from 'prop-types';

const Loading = ({ loading }) => {
 return (
    <Backdrop
      sx={{
        color: '#fff',
        zIndex: (theme) => theme.zIndex.drawer + 1
      }}
      open={loading}
    >
      <Paper
        sx={{
          outlined: 'none',
          borderRadius: 24,
          pl: 2,
          pr: 3,
          py: 2,
          gap: 3,
          display: 'flex',
          alignItems: 'center'
        }}
      >
        <CircularProgress color="primary" />
        <Typography>
          Cargando...
        </Typography>
      </Paper>
    </Backdrop>
 );
}

Loading.propTypes = {
 loading: PropTypes.bool.isRequired
};

export default Loading;
