import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Header from '../components/Header';
import Footer from '../components/Footer';
import { Box, Button, Divider, Typography } from '@mui/material';
import CommentView from '../components/Comment';
import { Post, PostComment, PostRequest } from '../models/Models';
import { useNavigate, useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';
import DeleteIcon from '@mui/icons-material/Delete';
import DoneIcon from '@mui/icons-material/Done';

const theme = createTheme();

export default function NewBlogPost() {
    let navigate = useNavigate();

    let [title, setTitle] = useState<string>("")
    let [content, setContent] = useState<string>("")

    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Container maxWidth="lg">
                <Header title="WeBlog" />
                <main>
                    <Typography
                        variant="h4"
                        gutterBottom
                        sx={{ fontWeight: 'bold' }}
                        suppressContentEditableWarning={true}
                        contentEditable={true}
                        onClick={(e) => {
                            if (title == "") {
                                e.currentTarget.textContent = ""
                            }
                        }}
                        onInput={(e) => {
                            let text = e.currentTarget.textContent;
                            if (text != null) {
                                setTitle(text);
                            }
                        }}
                    >
                        Title
                    </Typography>
                    <Typography
                        variant="body1"
                        suppressContentEditableWarning={true}
                        contentEditable={true}
                        onClick={(e) => {
                            if (content == "") {
                                e.currentTarget.textContent = ""
                            }
                        }}
                        onInput={(e) => {
                            let text = e.currentTarget.textContent;
                            if (text != null) {
                                setContent(text);
                            }
                        }}
                    >
                        Content
                    </Typography>
                    <Divider style={{ marginTop: 10, marginBottom: 10 }} />
                    <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between' }}>
                        <Button variant="outlined" size="large" style={{ marginRight: 5 }} onClick={() => {
                            let userId = localStorage.getItem("userId");
                            let token = localStorage.getItem("token");
                            if (userId != null && token != null) {
                                axios.post(`http://127.0.0.1:5000/user/${userId}/post`, {
                                    "title": title,
                                    "content": content
                                }, {
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
                        }}>
                            Done
                            <DoneIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                        <Button color='error' variant="outlined" size="large" onClick={() => {
                            navigate(-1)
                        }}>
                            Cancel
                            <DeleteIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                    </Box>
                </main>
            </Container>
            <Footer
                title="WeBlog"
                description="Ante&Filip, Erasmus 2022"
            />
        </ThemeProvider>
    )
}