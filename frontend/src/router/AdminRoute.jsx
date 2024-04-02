import { getRole, isLoggedIn } from "../utils/auth";
import PropTypes from "prop-types";
import { Navigate } from "react-router-dom";

export default function AdminRoute({ children }) {
  console.log(getRole());
  if (getRole() == "admin") {
    return <>{children}</>;
  } else {
    return <Navigate to="/" />;
  }
}

AdminRoute.propTypes = {
  children: PropTypes.node.isRequired,
};
