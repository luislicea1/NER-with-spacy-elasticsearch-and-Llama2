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
export default function NERContainer() {
  const [indices, setIndices] = useState();
  const [indicesNerResult, setIndicesNerResult] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(null);
  const [loading, setLoading] = useState(false); 
  const [loading_ner, setLoading_ner] = useState(false); 

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
    // setIndicesNerResult(data);
    setIndicesNerResult(JSON.stringify(data, null, 2)); // Convertir a string JSON
  }

  return (
    <Stack display={"flex"} flexDirection={"row"}>
      <Box
        boxShadow={10}
        borderRadius={2}
        width={"30vw"}
        height={"calc(100vh - 125px)"}
        margin={2}
        padding={2}
      >
        <Typography variant="h6" align="left" gutterBottom color="black">
          Prueba
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
        sx={{
          overflow: "hidden",
          overflowY: "scroll",
        }}
      >
        <Typography variant="h6" align="left" gutterBottom color="black">
          Resultado
        </Typography>
        <Divider></Divider>
        <Container>
          <section style={{ color: "black" }}>
            {loading_ner && <LinearProgress />}
            {indicesNerResult && <pre>{indicesNerResult}</pre>}
          </section>
        </Container>
      </Box>
    </Stack>
  );
}
