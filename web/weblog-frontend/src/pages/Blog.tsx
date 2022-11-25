import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from '../components/Header';
import FeaturedPost from '../components/FeaturedPost';
import Footer from '../components/Footer';
import { useEffect, useState } from 'react';
import { Post } from '../models/Models';
import axios from 'axios';

const theme = createTheme();

export default function Blog() {

  const [posts, setPosts] = useState<Post[] | null>(null)

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await axios.get('http://web-flask-appsec.herokuapp.com/post');
      let fetchedPosts = response.data as Post[];
      setPosts(fetchedPosts);
    };
    fetchPosts();
  }, []);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Header title="WeBlog" />
        <main>
          <Grid container spacing={4}>
            {posts != null && posts.map((post) => (
              <FeaturedPost key={post.id} post={post} />
            ))}
          </Grid>
        </main>
      </Container>
      <Footer
        title="WeBlog"
        description="Ante&Filip, Erasmus 2022"
      />
    </ThemeProvider>
  );
}