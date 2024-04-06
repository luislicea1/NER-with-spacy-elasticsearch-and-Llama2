import { Badge, Typography, Stack, Button, Container, LinearProgress, Box , Divider, Card, TextField} from "@mui/material";
import React, { useState, useEffect } from "react";
import { useTranslation } from 'react-i18next';

export default function PruebaContainer() {
    const [t,i18n] =useTranslation("global");
    const [inputData, setInputData] = useState({ message: "" });
    const [result, setResult] = useState(null);
    const [html, setHtml] = useState("");
    const [loading, setLoading] = useState(false); 
  
    async function handleSend() {
      console.log(JSON.stringify(inputData));
      setLoading(true);
      const response = await fetch("http://127.0.0.1:5000/new", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(inputData),
      });
      
      setLoading(false);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      } else {
        const data = await response.json();
        setResult(data);
        setHtml({ __html: data.message });
      }
    }
    
    return (
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
                    {t("content.test")}
                </Typography>
                <Divider></Divider>
                <Box marginTop={2}>
                    <TextField
                        id="outlined-multiline-static"
                        label="Write text"
                        multiline
                        rows={5}
                        fullWidth
                        value={inputData.message}
                        onChange={() => {
                            setInputData((prev) => {
                            const newPost = {
                                ...prev,
                                message: event.target.value,
                            };
                            return newPost;
                            });
                        }}
                    />
                    <Button onClick={handleSend} variant="contained" sx={{marginTop: "10px"}} >{t("btn.send")}</Button>
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
                    {t("content.result")}
                </Typography>
                <Divider></Divider>
                {loading && <LinearProgress></LinearProgress>}
                <Box marginTop={2}>
                    {result && (
                        <Box  color={'black'}>
                            {html.__html && (
                                <div dangerouslySetInnerHTML={html} />
                            )}
                        </Box>
                    )}
                </Box>
            </Box>
        </Stack>
    )
}