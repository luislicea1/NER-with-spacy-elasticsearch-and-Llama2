import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

function IndexNER() {
  //const [html, setHtml] = useState('');
  const [indices, setIndices] = useState();
  const [indicesNerResult, setIndicesNerResult] = useState(null);
  const [selectedIndex, setSelectedIndex] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch("http://localhost:5000/get-index");
      const data = await response.json();

      setIndices(data);
    };

    fetchData();
  }, []);

  useEffect(() => {}, [indicesNerResult]);

  async function onClickIndex(indice) {
    setSelectedIndex(indice);
    const response = await fetch("http://localhost:5000/ner-index-result", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ indice: indice }),
    });

    const data = await response.json();
    console.log(data);
    // setIndicesNerResult(data);
    setIndicesNerResult(JSON.stringify(data, null, 2)); // Convertir a string JSON
  }

  return (
    <>
      <div className="content">
        <Row>
          <Col md="12">
            <Card className="">
              <CardHeader>
                <CardTitle tag="h5">Name Entity Recognition</CardTitle>
              </CardHeader>
              <CardBody>
                <div style={{display: "flex", gap: "10px"}}>
                  {indices?.length > 0 &&
                    indices.map((indice) => {
                      const isSelected = selectedIndex === indice;
                      return (
                        <Card key={indice} style={{padding: "10px", border: "1px solid gray", backgroundColor: isSelected ? 'blue' : 'white', color: isSelected ? 'white' : 'black', cursor: "pointer"}}>
                          <span
                            onClick={() => {
                              onClickIndex(indice);
                            }}
                          >
                            {indice}
                          </span>
                        </Card>
                      );
                    })}
                </div>
                
                {/* <section>
                  {indicesNerResult &&
                    indicesNerResult.map((res) => {
                      return (
                        <>
                          <h5>{res.sentence}</h5>
                          {res.entities.map((entity) => {
                            return (
                              <section>
                                <span>Name : {entity.name} </span>
                                <span>Start : {entity.start} </span>
                                <span>End : {entity.end} </span>
                                <span>Label : {entity.label} </span>
                              </section>
                            );
                          })}
                        </>
                      );
                    })}
                </section> */}
                <section>
                  {indicesNerResult && <pre>{indicesNerResult}</pre>}
                </section>

              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default IndexNER;
