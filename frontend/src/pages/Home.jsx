import NavBar from "../components/NavBar";
import HomeContainer from "../components/Home/HomeContainer";
import { useTranslation } from 'react-i18next';

export default function Home(){
    const [t,i18n] =useTranslation("global");
    return(
        <>
            <NavBar title = {t("header.home")}></NavBar>
            <HomeContainer></HomeContainer>
        </>
    );
}