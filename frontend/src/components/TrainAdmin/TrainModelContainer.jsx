import { Badge, Typography, Stack, Button, LinearProgress, Box, Divider, TextField, Modal} from "@mui/material";
import React, { useState, useEffect } from "react";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useTranslation } from 'react-i18next';

export default function TrainModelContainer(){
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false); 
    const [t,i18n] =useTranslation("global");

    useEffect(() => {
        const fetchData = async () => {
          setLoading(true);
          const response = await fetch("http://localhost:5000/get_data_es_train_data");
          const data = await response.json();
    
          setResult(data);
          setLoading(false);
        };
    
        fetchData();
      }, []);
    
    async function onClickTrain() {
        setLoading(true);
        
        const requestOptions = {
            method: 'POST',
        };
        try {
            const response = await fetch("http://localhost:5000/train_model_spacy_admin", requestOptions);
            const responseData = await response.json();
            alert(responseData)
            setLoading(false);
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    async function onClickDeleteData() {
        setLoading(true);
        
        const requestOptions = {
            method: 'DELETE',
        };
        try {
            const response = await fetch("http://localhost:5000/delete_index_data_to_review", requestOptions);
            const responseData = await response.json();
            alert(responseData)
            setLoading(false);
        } catch (error) {
            console.error('Error:', error);
            setLoading(false);
        }
    }

    return(
        <Stack display={'flex'} flexDirection={{ xs: 'column', sm: 'row' }}>
            <Box
                boxShadow={10}
                borderRadius={2}
                width={"95vw"}
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
                    <Stack display={'flex'} flexDirection={'row'} gap={2}>
                        <Button variant="contained" onClick = {onClickDeleteData} sx={{marginBottom: "10px"}} disabled={!result || loading} color="error">{t("btn.delete_revision_data")}</Button>
                        <Button variant="contained" onClick = {onClickTrain} sx={{marginBottom: "10px"}} disabled={!result || loading}>{t("btn.train_model")}</Button>
                    </Stack>
                    
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
        </Stack>
    );
}