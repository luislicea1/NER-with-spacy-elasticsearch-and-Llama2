
import Dashboard from "views/Dashboard.js";
import Notifications from "views/Notifications.js";
import Icons from "views/Icons.js";
import TableList from "views/Tables.js";
import UserPage from "views/User.js";
import Ner from "views/Ner";
import Modelos from "views/Modelos";
import Reentrenamiento from "views/Reentrenamiento";
import Displacy from "views/Displacy";

var routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-bank",
    component: <Dashboard />,
    layout: "/admin",
  },
  {
    path: "/icons",
    name: "Icons",
    icon: "nc-icon nc-diamond",
    component: <Icons />,
    layout: "/admin",
  },
  
  {
    path: "/notifications",
    name: "Notifications",
    icon: "nc-icon nc-bell-55",
    component: <Notifications />,
    layout: "/admin",
  },
  {
    path: "/user-page",
    name: "User Profile",
    icon: "nc-icon nc-single-02",
    component: <UserPage />,
    layout: "/admin",
  },
  {
    path: "/tables",
    name: "Table List",
    icon: "nc-icon nc-tile-56",
    component: <TableList />,
    layout: "/admin",
  },
  
  {
    path: "/ner",
    name: "Ner",
    icon: "nc-icon nc-paper",
    component: <Ner />,
    layout: "/admin",
  },
  {
    path: "/modelos",
    name: "Modelos",
    icon: "nc-icon nc-paper",
    component: <Modelos />,
    layout: "/admin",
  },
  {
    path: "/reentrenamiento",
    name: "Reentrenamiento",
    icon: "nc-icon nc-paper",
    component: <Reentrenamiento />,
    layout: "/admin",
  },
  {
    path: "/displacy",
    name: "Displacy",
    icon: "nc-icon nc-paper",
    component: <Displacy />,
    layout: "/admin",
  },
  
];
export default routes;
