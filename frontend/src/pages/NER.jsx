import NavBar from "../components/NavBar";
import { Typography } from "@mui/material";
import NERContainer from "../components/NER/NERContainer";

export default function NER(){
    return(
        <>
            <NavBar title = "Name Entity Recognition"></NavBar>
            <NERContainer></NERContainer>
        </>
    );
}