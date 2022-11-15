import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Box, Button, Divider, Typography } from '@mui/material';
import CommentView from '../components/Comment';
import { Post, PostComment } from '../models/Models';
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import EditIcon from '@mui/icons-material/Edit';
import axios from 'axios';
import AddCommentView from '../components/AddComment';
import DeleteIcon from '@mui/icons-material/Delete';


const theme = createTheme();

export default function BlogPost() {

    let navigate = useNavigate();

    let { userId, postId } = useParams()
    const [post, setPost] = useState<Post | null>(null)
    const [comments, setComments] = useState<PostComment[] | null>(null)
    const [addComment, setAddComment] = useState<boolean>(false);

    const fetchComments = async () => {
        const response = await axios.get(`http://127.0.0.1:5000/user/${userId}/post/${postId}/comment`);
        let fetchedComments = response.data as PostComment[];
        setComments(fetchedComments)
    };

    const deleteComment = async (id: string) => {
        let token = localStorage.getItem("token");
        let myUserId = localStorage.getItem("userId");
        if (token != null && myUserId != null) {
            axios.delete(`http://127.0.0.1:5000/user/${myUserId}/post/${postId}/comment/${id}`, {
                headers: {
                    "Authorization": `Basic ${token}`
                }
            }).then(res => {
                if (res.status == 200) {
                    fetchComments()
                }
                if (res.status == 401) {
                    localStorage.clear()
                }
            })
        }
    }

    const updateComment = async (id: string, content: string) => {
        let token = localStorage.getItem("token");
        if (token != null) {
            axios.put(`http://127.0.0.1:5000/user/${userId}/post/${postId}/comment/${id}`,
                {
                    "content": content
                },
                {
                    headers: {
                        "Authorization": `Basic ${token}`
                    }
                }).then(res => {
                    if (res.status == 200) {
                        fetchComments()
                    }
                    if (res.status == 401) {
                        localStorage.clear()
                    }
                })
        }
    }

    const deletePost = async () => {
        let token = localStorage.getItem("token");
        if (token != null) {
            axios.delete(`http://127.0.0.1:5000/user/${userId}/post/${postId}`, {
                headers: {
                    "Authorization": `Basic ${token}`
                }
            }).then(res => {
                if (res.status == 200) {
                    navigate("/")
                }
                if (res.status == 401) {
                    localStorage.clear()
                }
            })
        }
    }

    useEffect(() => {
        const fetchPost = async () => {
            const response = await axios.get(`http://127.0.0.1:5000/user/${userId}/post/${postId}`);
            let fetchedPost = response.data as Post;
            setPost(fetchedPost);
        };
        fetchPost();
    }, []);

    useEffect(() => {
        fetchComments();
    }, [])

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Container maxWidth="lg">
                <Header title="WeBlog" />
                <main>
                    <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                        <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
                            {post?.title}
                        </Typography>
                        {
                            ((localStorage.getItem("isAdmin") != null && localStorage.getItem("isAdmin")) == "True" ||
                                (localStorage.getItem("userId") != null && localStorage.getItem("userId") == userId)) &&
                            <Button color='error' variant="outlined" size="small" onClick={() => { deletePost() }}>
                                Delete post
                                <DeleteIcon fontSize='small' style={{ marginLeft: 2 }} />
                            </Button>
                        }
                    </Box>
                    <Typography variant="subtitle1" color="text.secondary">
                        By: {post?.username}
                    </Typography>
                    <Typography variant="body1" marginTop={2}>
                        {post?.content}
                    </Typography>
                    <Divider style={{ marginTop: 10, marginBottom: 10 }} />
                    <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                            Comments
                        </Typography>
                        {localStorage.getItem("userId") != null &&
                            <Button variant="outlined" size="small" style={{ marginRight: 5 }} onClick={() => { setAddComment(true) }}>
                                Add new comment
                                <EditIcon fontSize='small' style={{ marginLeft: 2 }} />
                            </Button>
                        }
                    </Box>
                    {
                        addComment && postId != null &&
                        <AddCommentView postId={postId} cancelClick={() => { setAddComment(false) }} doneClick={() => {
                            fetchComments()
                            setAddComment(false)
                        }} />
                    }
                    <Divider style={{ marginTop: 10, marginBottom: 10 }} />
                    {comments != null && comments.map((comment) => (
                        <CommentView comment={comment} deleteClick={() => {
                            deleteComment(comment.id)
                        }} updateClick={(content: string) => {
                            updateComment(comment.id, content)
                        }} />
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