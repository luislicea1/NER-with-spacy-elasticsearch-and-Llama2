import { Badge, Typography, Stack, Button, LinearProgress, Box, Divider, TextField, Modal} from "@mui/material";
import React, { useState, useEffect } from "react";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useTranslation } from 'react-i18next';
import { getUser } from "../../utils/auth";

export default function TrainContainer(){
    const [inputData, setInputData] = useState({ entity: "", text: "" , entity_type: ""});
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false); 
    const [openModal, setOpenModal] = useState(false);
    const [t,i18n] =useTranslation("global");
    const user = getUser()

    const handleChange = (event) => {
        const { name, value } = event.target;
        setInputData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };
    
    async function onClickIndex() {
        setLoading(true);
        const response = await fetch("http://localhost:5000/generate-sentences", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(inputData),
        });

        const data = await response.json();
        console.log(data);
        setLoading(false);
        setResult(data); 
    }

    async function sendDataToSpecialist(){
        setLoading(true);
        const documents = Object.values(result);
        const data = { data: { data: { ...documents } } }; 
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        };
        try {
            const response = await fetch("http://localhost:5000/save_data_to_specialist", requestOptions);
            const responseData = await response.json();
            console.log(responseData);
            alert(responseData)
            setResult(null);
            setLoading(false);
            sendTrace("Envio dataset a especialista")
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    async function onClickTrain() {
        setLoading(true);
        const documents = Object.values(result);
        const data = { data: { data: { ...documents } } }; 
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        };
        try {
            const response = await fetch("http://localhost:5000/train_model_without_loss", requestOptions);
            const responseData = await response.json();
            alert(responseData);
            setResult(null);
            setLoading(false);
            sendTrace("Entreno modelo de reconocimiento de entidades")
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    const onClickTrainModel = () => {
        setOpenModal(true);
    }
    const handleModalAction = (action) => {
        setOpenModal(false);
        if (action === 'train') {
            onClickTrain();
        }
        else if (action === 'specialist'){
            sendDataToSpecialist();
        }
    }

    const sendTrace = async (action_type) => {
        const traceData = {
           username: user, 
           action_type: action_type
        };
       
        try {
           const response = await fetch('http://localhost:5000/traza', {
             method: 'POST',
             headers: {
               'Content-Type': 'application/json',
             },
             body: JSON.stringify(traceData),
           });
       
           if (!response.ok) {
             throw new Error('Error al enviar la traza');
           }
       
           const data = await response.json();
           console.log('Traza enviada con éxito:', data);
        } catch (error) {
           console.error('Error al enviar la traza:', error);
        }
       };
    

    return(
        <Stack display={'flex'} flexDirection={{ xs: 'column', sm: 'row' }}>
            <Box
                boxShadow={10}
                borderRadius={2}
                width={{xs: "80vw", sm: "30vw"}}
                height={'calc(100vh - 125px)'}
                margin={2}
                padding={2}
            >
                <Typography variant="h6" align="left" gutterBottom color="black" >
                    {t("content.generate_data_train")}
                </Typography>
                <Divider />
                <Box marginTop={2} display={'flex'} flexDirection={'column'} gap={"20px"}>
                    <TextField
                        id="entity"
                        name="entity"
                        label={t("input.write_new_entity")}
                        multiline
                        rows={1}
                        fullWidth
                        value={inputData.entity}
                        onChange={handleChange}
                    />
                    <TextField
                        id="text"
                        name="text"
                        label={t("input.write_entity_description")}
                        multiline
                        rows={5}
                        fullWidth
                        value={inputData.text}
                        onChange={handleChange}
                    />
                    <TextField
                        id="entity_type"
                        name="entity_type"
                        label={t("input.write_entity_type")}
                        multiline
                        rows={1}
                        fullWidth
                        value={inputData.entity_type}
                        onChange={handleChange}
                    />
                    <Button variant="contained" onClick={onClickIndex} sx={{marginTop: "10px"}} disabled={loading}>
                        {t("btn.send")}
                    </Button>
                </Box>
            </Box>

            <Box
                boxShadow={10}
                borderRadius={2}
                width={{xs: "80vw", sm: "65vw"}}
                height={'calc(100vh - 125px)'}
                margin={2}
                padding={2}
                sx={{
                    overflow: 'hidden',
                    overflowY: 'scroll',
                 }}
            >
                <Stack display={'flex'} flexDirection={'row'} justifyContent={'space-between'}>
                    <Typography variant="h6" align="left" gutterBottom color="black">
                        {t("content.result")}
                    </Typography>
                    <Button variant="contained" onClick={onClickTrainModel} sx={{marginBottom: "10px"}} disabled={!result || loading}>{t("btn.train_model")}</Button>
                </Stack>
                <Divider />
                {loading && <LinearProgress />}
                <Box marginTop={2}>
                    {result && (
                        <Box color={'black'}>
                            <SyntaxHighlighter language="json" style={dracula}>
                                {JSON.stringify(result, null, 4)}
                            </SyntaxHighlighter>
                        </Box>
                    )}
                </Box>
            </Box>

            {/* Modal */}
            <Modal
                open={openModal}
                onClose={() => setOpenModal(false)}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    width: 600,
                    bgcolor: 'background.paper',
                    boxShadow: 24,
                    p: 4,
                    
                }}>
                    <Typography id="modal-modal-title" variant="h6" component="h2" color={'black'}>
                        ¿Desea que un especialista haga el reentrenamiento?
                    </Typography>
                    <Box sx={{ mt: 2 }} display={'flex'} gap={2}>
                        <Button onClick={() => handleModalAction('cancel')} variant="outlined" color="error">{t("btn.cancel")}</Button>
                        <Button onClick={() => handleModalAction('specialist')} variant="contained" color="success">{t("btn.send_to_specialist")}</Button>
                        <Button onClick={() => handleModalAction('train')} variant="contained">{t("btn.train_model")}</Button>
                    </Box>
                </Box>
            </Modal>
        </Stack>
    );
}
