import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";

function Displacy() {
 const [html, setHtml] = useState('');

 useEffect(() => {
  fetch('http://localhost:5000/html')
    .then(response => response.text())
    .then(html => setHtml(html));
 }, []);

 return (
    <>
        <div className="content">
            <Row>
                <Col md="12">
                    <Card className="">
                        <CardHeader>
                            <CardTitle tag="h5">
                                Name Entity Recognition
                            </CardTitle>
                        </CardHeader>
                        <CardBody>
                            <div>
                                <section>
                                    <div dangerouslySetInnerHTML={{ __html: html }} />
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

export default Displacy;
