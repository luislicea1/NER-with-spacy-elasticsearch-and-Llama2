import NavBar from "../components/NavBar";
import TrainContainer from "../components/Train/TrainContainer";
import { useTranslation } from 'react-i18next';

export default function Train(){
    const [t,i18n] =useTranslation("global");
    return(
        <>
            <NavBar title={t("header.train")}></NavBar>
            <TrainContainer></TrainContainer>
        </>
    );
}