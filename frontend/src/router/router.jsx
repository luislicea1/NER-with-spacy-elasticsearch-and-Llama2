import { lazy } from "react";
import { createBrowserRouter, Outlet } from "react-router-dom";
import ProtectedRouter from "./ProtectedRouter";
import AdminRoute from "./AdminRoute";

const Root = lazy(() => import("../components/Root"));
const Home = lazy(() => import("../pages/Home"));
const NER = lazy(() => import("../pages/NER"));
const Train = lazy(() => import("../pages/Train"));
const Prueba = lazy(() => import("../pages/Prueba"));
const ErrorPage = lazy(() => import("../pages/ErrorPage"));
const Login = lazy(() => import("../pages/Login"));
const UsersAdmin = lazy(() => import("../pages/UsersAdmin"));

export const router = createBrowserRouter([
  {
    path: "/",
    element: <Root />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "",
        element: (
          <ProtectedRouter>
            <Outlet />
          </ProtectedRouter>
        ),
        children: [
          {
            index: true,
            element: <Home />,
          },
          {
            path: "ner",
            element: <NER />,
          },
          {
            path: "train",
            element: <Train />,
          },
          {
            path: "prueba",
            element: <Prueba />,
          },
          {
            path: "users_admin",
            element: (
              <AdminRoute>
                <UsersAdmin />
              </AdminRoute>
            ),
          },
        ],
      },
      {
        path: "login",
        element: <Login />,
      },
    ],
  },
]);
