import React from "react";
import NavBar from "../components/NavBar";
import UsersAdminContainer from "../components/UsersAdmin/UsersAdminContainer";
import { useTranslation } from 'react-i18next';

export default function UsersAdmin(){
    const [t,i18n] =useTranslation("global");
    return (
        <>
            <NavBar title={t("header.user_admin")}></NavBar>
            <UsersAdminContainer></UsersAdminContainer>
        </>
    )
}