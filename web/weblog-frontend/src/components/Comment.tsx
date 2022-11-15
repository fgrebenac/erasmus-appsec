import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { Button, Divider } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import DoneIcon from '@mui/icons-material/Done';
import EditIcon from '@mui/icons-material/Edit';
import { useState } from 'react';
import { PostComment } from '../models/Models';

interface CommentProps {
    comment: PostComment,
    deleteClick: () => any,
    updateClick: (content: string) => any,
}

export default function CommentView({ comment, deleteClick, updateClick }: CommentProps) {

    const [isEditing, setEditing] = useState<boolean>(false);
    let [content, setContent] = useState<string>(comment.content)

    return (
        <Box>
            <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 1 }}>
                <Typography variant="body1" sx={{ fontFamily: "bold" }}>
                    {comment.username}
                </Typography>
                <Box>
                    {!isEditing && localStorage.getItem("userId") != null && localStorage.getItem("userId") === comment.user_id &&
                        <Button variant="outlined" size="small" style={{ marginRight: 5 }} onClick={() => { setEditing(true) }}>
                            Edit
                            <EditIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                    }
                    {isEditing && localStorage.getItem("userId") != null && localStorage.getItem("userId") === comment.user_id &&
                        <Button variant="outlined" size="small" style={{ marginRight: 5 }} onClick={() => {
                            updateClick(content);
                            setEditing(false)
                        }}>
                            Done
                            <DoneIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                    }
                    {
                        ((localStorage.getItem("isAdmin") != null && localStorage.getItem("isAdmin") === "True") ||
                        (localStorage.getItem("userId") != null && localStorage.getItem("userId") === comment.user_id)) &&
                        <Button color='error' variant="outlined" size="small" onClick={() => { deleteClick() }}>
                            Delete
                            <DeleteIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                    }
                </Box>
            </Box>
            <Typography
                variant="body1"
                suppressContentEditableWarning={true}
                contentEditable={isEditing}
                onInput={(e) => {
                    let text = e.currentTarget.textContent;
                    if (text != null) {
                        setContent(text);
                    }
                }}
                marginRight="10px">
                {comment.content}
            </Typography>
            <Divider style={{ marginTop: 10, marginBottom: 10 }} />
        </Box>
    );
}