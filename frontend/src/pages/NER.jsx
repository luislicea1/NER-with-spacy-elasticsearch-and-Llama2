import NavBar from "../components/NavBar";
import { Typography } from "@mui/material";
import NERContainer from "../components/NER/NERContainer";
import { useTranslation } from 'react-i18next';

export default function NER(){
    const [t,i18n] =useTranslation("global");

    return(
        <>
            <NavBar title = {t("header.name_entity_recognition")}></NavBar>
            <NERContainer></NERContainer>
        </>
    );
}