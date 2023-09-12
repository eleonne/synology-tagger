import React from "react";

import { Icon } from "@chakra-ui/react";
import {
  MdBarChart,
  MdSettings,
  MdHome,
  MdLock,
  MdOutlineShoppingCart,
} from "react-icons/md";

// Admin Imports
import MainDashboard from "views/admin/default";
// import NFTMarketplace from "views/admin/marketplace";
// import Profile from "views/admin/profile";
import DataTables from "views/admin/dataTables";
import Wizard from "views/admin/wizard";
// import RTL from "views/admin/rtl";

// Auth Imports
import SignInCentered from "views/auth/signIn";

const routes = [
  {
    name: "Dashboard",
    layout: "/admin",
    path: "/default",
    icon: <Icon as={MdHome} width='20px' height='20px' color='inherit' />,
    component: MainDashboard,
  },
  {
    name: "Details",
    layout: "/admin",
    icon: <Icon as={MdBarChart} width='20px' height='20px' color='inherit' />,
    path: "/data-tables",
    component: DataTables,
  },
  {
    name: "Configuration",
    layout: "/admin",
    icon: <Icon as={MdSettings} width='20px' height='20px' color='inherit' />,
    path: "/wizard",
    component: Wizard,
  }
];

export default routes;
