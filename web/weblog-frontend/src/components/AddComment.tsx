import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Button, Divider } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import DoneIcon from '@mui/icons-material/Done';
import axios from 'axios';
import { useState } from 'react';

interface AddCommentProps {
    postId: string,
    cancelClick: () => any,
    doneClick: () => any,
}

export default function AddCommentView({ postId, cancelClick, doneClick }: AddCommentProps) {

    let [content, setContent] = useState<string>("Write comment...")

    return (
        <Box>
            <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 1 }}>
                <Box>
                    <Button variant="outlined" size="small" style={{ marginRight: 5 }} onClick={() => {
                        let userId = localStorage.getItem("userId");
                        let token = localStorage.getItem("token");
                        if (userId != null && token != null) {
                            axios.post(`http://127.0.0.1:5000/user/${userId}/post/${postId}/comment`, {
                                "content": content,
                            }, {
                                headers: {
                                    "Authorization": `Basic ${token}`
                                }
                            }).then(res => {
                                if (res.status == 200) {
                                    doneClick()
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
                    <Button color='error' variant="outlined" size="small" onClick={() => { cancelClick() }}>
                        Cancel
                        <DeleteIcon fontSize='small' style={{ marginLeft: 2 }} />
                    </Button>
                </Box>
            </Box>
            <Typography
                variant="body1"
                suppressContentEditableWarning={true}
                contentEditable={true}
                onInput={(e) => {
                    let text = e.currentTarget.textContent;
                    if (text != null) {
                        setContent(text);
                    }
                }}
                marginRight="10px">
                Write comment...
            </Typography>
            <Divider style={{ marginTop: 10, marginBottom: 10 }} />
        </Box>
    );
}