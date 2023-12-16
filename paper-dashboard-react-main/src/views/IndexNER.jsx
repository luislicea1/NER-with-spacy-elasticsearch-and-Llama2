import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

function IndexNER() {
  //const [html, setHtml] = useState('');
  const [indices, setIndices] = useState();
  const [indicesNerResult, setIndicesNerResult] = useState(null);

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
    const response = await fetch("http://localhost:5000/ner-index-result", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ indice: indice }),
    });

    const data = await response.json();
    console.log(data);
    setIndicesNerResult(data);
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
                {indices?.length > 0 &&
                  indices.map((indice) => {
                    return (
                      <Card key={indice}>
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
                <section>
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
