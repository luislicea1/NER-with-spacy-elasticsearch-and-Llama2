import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";
import { inputStyle, buttonStyle } from "styles/style";

function Prueba() {
  const [inputData, setInputData] = useState({ message: "" });
  const [result, setResult] = useState(null);
  const [html, setHtml] = useState("");

  async function handleSend() {
    console.log(JSON.stringify(inputData));
    const response = await fetch("http://127.0.0.1:5000/new", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(inputData),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    } else {
      const data = await response.json();
      setResult(data);
      setHtml({ __html: data.message });
    }
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
                    <>
                      <div className="card">
                        <textarea
                          type="text"
                          style={inputStyle}
                          value={inputData.message}
                          placeholder="Texto para el reconocimento de entidades"
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
                        <button onClick={handleSend} style={buttonStyle}> ENVIAR FORM </button>
                      </div>
                     
                      {result && (
                        <>
                           <h4 className="read-the-docs">
                        Resultado de la peticion
                      </h4>
                          {html.__html && (
                            <div dangerouslySetInnerHTML={html} />
                          )}
                        </>
                      )}
                    </>
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

export default Prueba;

