import NavBar from "../components/NavBar";
import TrainModelContainer from "../components/TrainAdmin/TrainModelContainer";
import { useTranslation } from 'react-i18next';

export default function TrainModelAdmin(){
    const [t,i18n] =useTranslation("global");
    return(
        <>
            <NavBar title={t("header.train_model_admin")}></NavBar>
            <TrainModelContainer></TrainModelContainer>
        </>
    );
}