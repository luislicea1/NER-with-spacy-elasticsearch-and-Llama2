import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

function Reentrenamiento() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch("http://localhost:5000/")
      .then((response) => response.json())
      .then((data) => setData(data));
  }, []);

  if (!data) {
    return <div>Loading...</div>;
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
                <div>
                  <section>
                    <div>
                      {Object.entries(data).map(([key, value]) => (
                        <div key={key}>
                          <h2>Documento: {key}</h2>
                          <p>Texto: {value.text}</p>
                          <h3>Entidades:</h3>
                          <ul>
                            {value.entities.map((entity, index) => (
                              <li key={index}>
                                Nombre: {entity.name}, Inicio: {entity.start},
                                Fin: {entity.end}, Etiqueta: {entity.label}
                              </li>
                            ))}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </section>
                </div>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Reentrenamiento;
