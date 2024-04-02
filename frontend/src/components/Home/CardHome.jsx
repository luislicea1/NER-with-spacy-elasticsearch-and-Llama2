import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function MediaCard(props) {
  return (
    <Card sx={{ width: "100%"}}>
      <CardMedia sx={{width: "100%", display: "grid", placeItems: "center", padding: "20px"}}>
            <img src={props.imagen} alt="" />
      </CardMedia>
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {props.title}
        </Typography>
        <Typography variant="body2" color="text.secondary">
          {props.text}
        </Typography>
      </CardContent>
      <CardActions>
        <Button size="small" href={props.url}>View</Button>
      </CardActions>
    </Card>
  );
}