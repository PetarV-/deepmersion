import React from "react";
import { Label } from "react-bootstrap";

export const TagList = props => {
  let tags = props.tags.map(x => {
    return (
      <span>
        <Label bsStyle={props.bsStyle}>{x}</Label>
        &emsp;
      </span>
    );
  });

  return <p style={{ lineHeight: 1.75 }}>{tags}</p>;
};
