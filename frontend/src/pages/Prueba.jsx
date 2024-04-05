import NavBar from "../components/NavBar";
import PruebaContainer from "../components/Prueba/PruebaContainer";
import { useTranslation } from 'react-i18next';

export default function Prueba(){
    const [t,i18n] =useTranslation("global");
    return(
        <>
            <NavBar title= {t("header.test")}></NavBar>
            <PruebaContainer></PruebaContainer>
        </>
    );
}