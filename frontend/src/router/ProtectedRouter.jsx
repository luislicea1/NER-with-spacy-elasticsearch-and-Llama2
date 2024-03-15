import { isLoggedIn } from '../utils/auth';
import PropTypes from 'prop-types';
import { Navigate } from 'react-router-dom'

export default function ProtectedRouter({ children }) {
    if (!isLoggedIn()) {
        return <Navigate to="/login" />
    }
    return <>{children}</>
}

ProtectedRouter.propTypes = {
    children: PropTypes.node.isRequired,
};