import { Badge, Typography, Stack, Button, Container, LinearProgress, Box, Divider, TextField } from "@mui/material";
import React, { useState, useEffect } from "react";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';

export default function TrainContainer(){
    const [inputData, setInputData] = useState({ entity: "", text: "" , entity_type: ""});
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false); 

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
                    Generate Data Train
                </Typography>
                <Divider />
                <Box marginTop={2} display={'flex'} flexDirection={'column'} gap={"20px"}>
                    <TextField
                        id="entity"
                        name="entity"
                        label="Write new entity"
                        multiline
                        rows={1}
                        fullWidth
                        value={inputData.entity}
                        onChange={handleChange}
                    />
                    <TextField
                        id="text"
                        name="text"
                        label="Write entity description"
                        multiline
                        rows={5}
                        fullWidth
                        value={inputData.text}
                        onChange={handleChange}
                    />
                    <TextField
                        id="entity_type"
                        name="entity_type"
                        label="Write entity type"
                        multiline
                        rows={1}
                        fullWidth
                        value={inputData.entity_type}
                        onChange={handleChange}
                    />
                    <Button variant="contained" onClick={onClickIndex} sx={{marginTop: "10px"}} >
                        Send
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
                <Typography variant="h6" align="left" gutterBottom color="black">
                    Result
                </Typography>
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
