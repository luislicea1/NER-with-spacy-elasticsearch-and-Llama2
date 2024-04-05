import React,{useEffect, useState} from "react";
import {
    Typography,
    Stack,
    Button,
    Box,
    Divider,
    Modal,
  } from "@mui/material";

import MediaCard from "./CardHome";
import imagen_ner from '../../assets/ner.svg'
import imagen_test from '../../assets/test.svg'
import imagen_fine from '../../assets/ia.svg'
import { useTranslation } from 'react-i18next';

export default function HomeContainer(){
    const [loading, setLoading] = useState(false); 
    const [initialTestDataMessage, setInitialTestDataMessage] = useState(null);
    const [openModal, setOpenModal] = useState(false); 
    const [modalMessage, setModalMessage] = useState('');
    const [t,i18n] =useTranslation("global");

    async function onClickSendInitialTest(message) {
        setInitialTestDataMessage(message);
        setLoading(true)
        const response = await fetch("http://localhost:5000/add_test_data", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ click: message }),
        });
    
        const data = await response.json();
        console.log(data);
        setModalMessage(data);
        setOpenModal(true);
        setLoading(false)
      }
    
    const handleCloseModal = () => {
        setOpenModal(false);
    };

    return(
        <Stack display={'flex'} flexDirection={'column'} paddingTop={3} paddingLeft={15} paddingRight={15}>
            <Typography variant="h4" align="left" gutterBottom color="black">
                {t("home.welcome")}
            </Typography>
            <Stack display={'flex'} flexDirection={'row'} gap={5} marginBottom={3}>
                <MediaCard url = "/ner" title = {t("home.name_entity_recognition")} imagen = {imagen_ner} text = {t("home.name_entity_recognition_container")}/>
                <MediaCard url = "/train" title = {t("home.fine_tunning_model")} imagen = {imagen_fine} text = {t("home.fine_tunning_model_container")}/>
                <MediaCard url = "/prueba" title = {t("home.testing_space")}imagen = {imagen_test} text = {t("home.testing_space_container")}/>
            </Stack>
            <Divider></Divider>
            <Stack display={'flex'} flex={'column'} marginTop={3}>
                <Typography variant="h4" align="left" gutterBottom color="black">
                    {t("home.get_started")}
                </Typography>
                <Typography variant="p" align="left" gutterBottom color="black">
                    {t("home.get_started_container")}
                </Typography>
                <Button variant="contained" sx={{width: "200px", marginTop: "10px"}} onClick={() => onClickSendInitialTest("click")} >
                    {t("btn.add_test_data")}
                </Button>


                <Modal
                    open={openModal}
                    onClose={handleCloseModal}
                    aria-labelledby="modal-title"
                    aria-describedby="modal-description"
                >
                    <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: 400,
                    bgcolor: 'background.paper',
                    boxShadow: 24,
                    p: 4,
                    }}>
                    <Typography id="modal-title" variant="h6" component="h2" color={'black'}>
                        Results
                    </Typography>
                    <Typography id="modal-description" sx={{ mt: 2 }} color={'black'}>
                        {modalMessage}
                    </Typography>
                    </Box>
                </Modal>

            </Stack>
        </Stack>
    )
}