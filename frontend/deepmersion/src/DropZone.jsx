import React, { Component } from "react";
import { Grid, Row, Col } from "react-bootstrap";

import request from "superagent";
import Dropzone from "react-dropzone";

import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faFileImage from "@fortawesome/fontawesome-free-regular/faFileImage";

import { TagList } from "./TagList";

export class DropZone extends Component {
  constructor(props) {
    super(props);

    this.state = {
      objectTags: [],
      placeTags: []
    };
  }

  classify = image => {
    request
      .post("/classify")
      .field("useObjects", this.props.useObjects)
      .field("useChatter", this.props.useChatter)
      .field("usePlaces", this.props.usePlaces)
      .attach("image", image)
      .then(res => {
        let objectTags = res.body.objectTags;
        let placeTags = res.body.placeTags;

        let volumes = res.body.volumes;
        this.props.onClassify(volumes);

        this.setState({
          objectTags: objectTags || [],
          placeTags: placeTags || []
        });
      });
  };

  onDrop = (accepted, rejected) => {
    // ask the server for an audio configuration
    this.classify(accepted[0]);

    // update the preview
    let reader = new FileReader();

    reader.onload = img => {
      console.log("image loaded");
      this.refs.preview.src = img.target.result;
    };
    reader.readAsDataURL(accepted[0]);
  };

  render() {
    return (
      <div className="container dragdrop">
        <Grid>
          <Row>
            <Col md={4}>
              <Dropzone
                accept="image/jpeg, image/png"
                multiple={false}
                onDrop={this.onDrop}
              >
                <div className="dropzone">
                  <FontAwesomeIcon icon={faFileImage} size="6x" />

                  <p>Drop an image here.</p>
                  <small>Accepts JPEG, PNG</small>
                </div>
              </Dropzone>
            </Col>
            <Col md={4}>
              <img ref="preview" className="previewImage" alt="" />
            </Col>
            <Col md={4}>
              <TagList tags={this.state.objectTags} bsStyle="primary" />
              <TagList tags={this.state.placeTags} bsStyle="success" />
            </Col>
          </Row>
        </Grid>
      </div>
    );
  }
}
