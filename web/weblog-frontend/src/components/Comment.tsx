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
    comment: PostComment
}

export default function CommentView({ comment }: CommentProps) {

    const [isEditing, setEditing] = useState<boolean>(false);

    return (
        <Box>
            <Box sx={{ display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 1 }}>
                <Typography variant="body1" sx={{ fontFamily: "bold" }}>
                    {comment.username}
                </Typography>
                <Box>
                    {!isEditing &&
                        <Button variant="outlined" size="small" style={{ marginRight: 5 }} onClick={() => { setEditing(true) }}>
                            Edit
                            <EditIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                    }
                    {isEditing &&
                        <Button variant="outlined" size="small" style={{ marginRight: 5 }} onClick={() => { setEditing(false) }}>
                            Done
                            <DoneIcon fontSize='small' style={{ marginLeft: 2 }} />
                        </Button>
                    }
                    <Button color='error' variant="outlined" size="small">
                        Delete
                        <DeleteIcon fontSize='small' style={{ marginLeft: 2 }} />
                    </Button>
                </Box>
            </Box>
            <Typography variant="body1" contentEditable={isEditing} marginRight="10px">
                {comment.content}
            </Typography>
            <Divider style={{ marginTop: 10, marginBottom: 10 }} />
        </Box>
    );
}