import React from "react";
import { Grid, Row, Col } from "react-bootstrap";

export const ImageChooser = props => {
  let imgs = props.imgs.map((url, i) => {
    return (
      <Col md={1} xs={4} key={i}>
        <img
          src={url}
          style={{ width: 50, height: 50 }}
          onClick={props.onSelect.bind(null, i)}
        />
      </Col>
    );
  });

  return (
    <Grid style={{ marginTop: 20 }}>
      <Row>{imgs}</Row>
    </Grid>
  );
};
