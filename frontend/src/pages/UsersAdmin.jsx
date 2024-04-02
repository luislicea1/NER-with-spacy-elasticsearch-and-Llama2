import React from "react";
import NavBar from "../components/NavBar";
import UsersAdminContainer from "../components/UsersAdmin/UsersAdminContainer";

export default function UsersAdmin(){
    return (
        <>
            <NavBar title="Users Admin"></NavBar>
            <UsersAdminContainer></UsersAdminContainer>
        </>
    )
}