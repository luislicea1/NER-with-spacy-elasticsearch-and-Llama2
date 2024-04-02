import React,{useEffect, useState} from "react";
import {
    Badge,
    Typography,
    Stack,
    Button,
    Container,
    LinearProgress,
    Box,
    Divider,
    Card,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Modal,
    Alert
  } from "@mui/material";

import MediaCard from "./CardHome";
import imagen_ner from '../../assets/ner.svg'
import imagen_test from '../../assets/test.svg'
import imagen_fine from '../../assets/ia.svg'

export default function HomeContainer(){
    const [loading, setLoading] = useState(false); 
    const [initialTestDataMessage, setInitialTestDataMessage] = useState(null);
    const [openModal, setOpenModal] = useState(false); 
    const [modalMessage, setModalMessage] = useState('');

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
                Welcome Home
            </Typography>
            <Stack display={'flex'} flexDirection={'row'} gap={5} marginBottom={3}>
                <MediaCard url = "/ner" title = "Name Entity Recognition" imagen = {imagen_ner} text = "Perform entity recognition with Spacy and index it back to Elasticsearch "/>
                <MediaCard url = "/train" title = "Fine Tunning Model" imagen = {imagen_fine} text = "Retrain the Spacy model so that it recognizes new entities without loss of knowledge"/>
                <MediaCard url = "/prueba" title = "Testing Space" imagen = {imagen_test} text = "We have testing space for documents that are not in elasticsearch"/>
            </Stack>
            <Divider></Divider>
            <Stack display={'flex'} flex={'column'} marginTop={3}>
                <Typography variant="h4" align="left" gutterBottom color="black">
                    Get started adding test data
                </Typography>
                <Typography variant="p" align="left" gutterBottom color="black">
                    Initial test data to test named entity recognition and indexing in elasticsearch
                </Typography>
                <Button variant="contained" sx={{width: "200px", marginTop: "10px"}} onClick={() => onClickSendInitialTest("click")} >
                    Add test data
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