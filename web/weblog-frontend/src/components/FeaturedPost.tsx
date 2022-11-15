import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import Card from '@mui/material/Card';
import CardActionArea from '@mui/material/CardActionArea';
import CardContent from '@mui/material/CardContent';
import { Post } from '../models/Models';
import { useNavigate } from 'react-router-dom';

interface FeaturedPostProps {
  post: Post
}

export default function FeaturedPost(props: FeaturedPostProps) {
  const { post } = props;
  let navigate = useNavigate();

  return (
    <Grid item xs={12} md={6}>
      <CardActionArea component="a" href="#" onClick={() => { navigate(`/user/${post.user_id}/post/${post.id}`) }}>
        <Card sx={{ display: 'flex' }}>
          <CardContent sx={{ flex: 1 }}>
            <Typography component="h2" variant="h5">
              {post.title}
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              {post.username}
            </Typography>
            {
              post.content.length > 50 ?
                <Typography variant="subtitle1" paragraph>
                  {post.content.substring(0, 60).concat("...")}
                </Typography>
                :
                <Typography variant="subtitle1" paragraph>
                  {post.content}
                </Typography>
            }
          </CardContent>
        </Card>
      </CardActionArea>
    </Grid>
  );
}