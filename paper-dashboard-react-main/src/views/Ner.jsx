import { Card, CardHeader, CardBody, CardTitle, Row, Col } from "reactstrap";
import axios from 'axios';
import { useEffect, useState } from "react";

export default function Ner(){

    const [result, setResult] = useState(null);

    const message = async() => {
        try{
            let res = await axios.get('http://127.0.0.1:5000/')
            let result = res.data;
            setResult(result);
        }catch(e){
            console.log(e)
        }
    }

    useEffect(() => {
        message()
    }, [])

    return(
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
                                    {result}
                                </section>
                            </div>
                        </CardBody>
                    </Card>

                </Col>
            </Row>
        </div>
           
        </>
    )
}