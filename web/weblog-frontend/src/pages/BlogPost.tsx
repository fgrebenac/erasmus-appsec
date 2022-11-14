import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Divider, Typography } from '@mui/material';
import CommentView from '../components/Comment';
import { Post, PostComment } from '../models/Models';
import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

const theme = createTheme();

export default function BlogPost() {

    let { postId } = useParams()
    const [post, setPost] = useState<Post | null>(null)
    const [comments, setComments] = useState<PostComment[] | null>(null)

    useEffect(() => {
        const fetchPost = async () => {
            console.log(postId);
            let userId = localStorage.getItem("userId")
            const response = await axios.get(`http://127.0.0.1:5000/user/${userId}/post/${postId}`);
            let fetchedPost = response.data as Post;
            setPost(fetchedPost);
        };
        fetchPost();
    }, []);

    useEffect(() => {
        const fetchComments = async () => {
            let userId = localStorage.getItem("userId")
            const response = await axios.get(`http://127.0.0.1:5000/user/${userId}/post/${postId}/comment`);
            let fetchedComments = response.data as PostComment[];
            setComments(fetchedComments)
        };
        fetchComments();
    }, [])

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Container maxWidth="lg">
                <Header title="WeBlog" />
                <main>
                    <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
                        {post?.title}
                    </Typography>
                    <Typography variant="body1">
                        {post?.content}
                    </Typography>
                    <Divider style={{ marginTop: 10, marginBottom: 10 }} />
                    <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                        Comments
                    </Typography>
                    <Divider style={{ marginTop: 10, marginBottom: 10 }} />
                    {comments != null && comments.map((comment) => (
                        <CommentView comment={comment} />
                    ))}
                </main>
            </Container>
            <Footer
                title="WeBlog"
                description="Ante&Filip, Erasmus 2022"
            />
        </ThemeProvider>
    )
}