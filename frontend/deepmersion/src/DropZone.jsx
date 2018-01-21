import React, { Component } from "react";
import { Grid, Row, Col } from "react-bootstrap";

import request from "superagent";
import Dropzone from "react-dropzone";

import FontAwesomeIcon from "@fortawesome/react-fontawesome";
import faFileImage from "@fortawesome/fontawesome-free-regular/faFileImage";

import { TagList } from "./TagList";
import { ImageChooser } from "./ImageChooser";

export class DropZone extends Component {
  constructor(props) {
    super(props);

    this.images = [
      "https://static.pexels.com/photos/103567/pexels-photo-103567.jpeg",
      "https://static.pexels.com/photos/688019/pexels-photo-688019.jpeg",
      "https://upload.wikimedia.org/wikipedia/commons/f/f6/White-noise-mv255-240x180.png",
      "https://static.pexels.com/photos/299113/pexels-photo-299113.jpeg",
      "https://static.pexels.com/photos/355989/pexels-photo-355989.jpeg",
      "https://static.pexels.com/photos/7763/pexels-photo.jpg",
      "https://static.pexels.com/photos/374592/pexels-photo-374592.jpeg",
      "https://static.pexels.com/photos/357316/pexels-photo-357316.jpeg",
      "https://static.pexels.com/photos/10467/pexels-photo-10467.jpeg",
      "https://static.pexels.com/photos/67826/jellyfish-luminous-jellyfish-light-light-phenomenon-67826.jpeg",
      "https://static.pexels.com/photos/164186/pexels-photo-164186.jpeg",
      "https://static.pexels.com/photos/162320/polar-bear-ice-arctic-white-162320.jpeg"
    ];

    this.state = {
      objectTags: [],
      placeTags: []
    };
  }

  onImageSelect = index => {
    this.refs.preview.src = this.images[index];
    this.classify(this.images[index]);
  };

  classify = image => {
    let req = request
      .post("/classify")
      .field("useObjects", this.props.useObjects)
      .field("useChatter", this.props.useChatter)
      .field("usePlaces", this.props.usePlaces)
      .field("chatterLevel", this.props.chatterLevel);

    if (typeof image === "string") {
      req.field("image_url", image);
    } else {
      req.attach("image", image);
    }

    req.then(res => {
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
      <div>
        <div className="container">
          <ImageChooser
            alt=""
            imgs={this.images}
            onSelect={this.onImageSelect}
          />
        </div>
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
                <img
                  ref="preview"
                  className="previewImage"
                  alt=""
                  style={{ objectFit: "cover" }}
                />
              </Col>
              <Col md={4}>
                <TagList tags={this.state.objectTags} bsStyle="primary" />
                <TagList tags={this.state.placeTags} bsStyle="success" />
              </Col>
            </Row>
          </Grid>
        </div>
      </div>
    );
  }
}
