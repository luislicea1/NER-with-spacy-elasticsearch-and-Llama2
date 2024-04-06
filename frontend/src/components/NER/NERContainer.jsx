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
} from "@mui/material";
import React, { useState, useEffect } from "react";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { useTranslation } from 'react-i18next';
import { getUser } from "../../utils/auth";

export default function NERContainer() {
  const [indices, setIndices] = useState();
  const [indicesNerResult, setIndicesNerResult] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [loading, setLoading] = useState(false); 
  const [loading_ner, setLoading_ner] = useState(false); 
  const [t,i18n] =useTranslation("global");
  const user = getUser()

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const response = await fetch("http://localhost:5000/get-index");
      const data = await response.json();

      setIndices(data);
      setLoading(false);
    };

    fetchData();
  }, []);

  useEffect(() => {}, [indicesNerResult]);

  async function onClickIndex(indice) {
    setSelectedIndex(indice);
    setLoading_ner(true)
    const response = await fetch("http://localhost:5000/ner-index-result", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ indice: indice }),
    });

    const data = await response.json();
    console.log(data);
    setLoading_ner(false)
    setIndicesNerResult(JSON.stringify(data, null, 2)); // Convertir a string JSON
  }

  async function saveInElastic() {
    if (!selectedIndex || !indicesNerResult) {
       alert("Por favor, selecciona un índice y obtén resultados antes de guardar.");
       return;
    }
   
    setLoading(true);
    try {
       const response = await fetch("http://localhost:5000/save_in_elastic", {
         method: "POST",
         headers: {
           "Content-Type": "application/json",
         },
         body: JSON.stringify({
           indice: selectedIndex,
           data: JSON.parse(indicesNerResult), 
         }),
       });
   
       if (!response.ok) {
         throw new Error("Error al guardar en Elasticsearch");
       }else{
          sendTrace()
       }
   
       const data = await response.json();
       alert("Datos guardados exitosamente");
    } catch (error) {
       alert(`Error: ${error.message}`);
    } finally {
       setLoading(false);
    }
   }


   const sendTrace = async () => {
    const traceData = {
       username: user, 
       action_type: "Salvo indice de elasticsearch luego de realizar el NER", 
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

  return (
    <Stack display={"flex"} flexDirection={"row"}>
      <Box
        boxShadow={10}
        borderRadius={2}
        width={"30vw"}
        height={"calc(100vh - 125px)"}
        margin={2}
        padding={2}
        sx={{
          overflow: "hidden",
          overflowY: "scroll",
        }}
      >
        <Typography variant="h6" align="left" gutterBottom color="black">
          {t("content.test")}
        </Typography>
        <Divider></Divider>
        <TableContainer>
        {loading && <LinearProgress />}
          <Table>
            <TableBody>
              {indices?.length > 0 &&
                indices.map((indice) => {
                  const isSelected = selectedIndex === indice;
                  return (
                    <TableRow
                      key={indice}
                      sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
                      style={{ cursor: "pointer" }}
                    >
                      <TableCell>{indice}</TableCell>
                      <TableCell>
                        <PlayArrowIcon
                          color="primary"
                          onClick={() => onClickIndex(indice)}
                        ></PlayArrowIcon>
                      </TableCell>
                    </TableRow>
                  );
                })}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
      <Box
        boxShadow={10}
        borderRadius={2}
        width={"65vw"}
        height={"calc(100vh - 125px)"}
        margin={2}
        padding={2}
        paddingTop={1}
        sx={{
          overflow: "hidden",
          overflowY: "scroll",
        }}
      >
        <Stack display={"flex"} flexDirection={"row"} justifyContent = {"space-between"} paddingBottom={1}>
          <Typography variant="h6" align="left" gutterBottom color="black">
            {t("content.result")}
          </Typography>

          <Button color="primary" variant="contained" onClick={saveInElastic}>{t("btn.save_in_elastic")}</Button>
        </Stack>
        <Divider></Divider>
        <Container>
          <section style={{ color: "black" }}>
            {loading_ner && <LinearProgress />}
            
            {indicesNerResult && (
              <SyntaxHighlighter language="json" style={dracula}>
                {indicesNerResult}
              </SyntaxHighlighter>
            )}
          </section>
        </Container>
      </Box>
    </Stack>
  );
}
