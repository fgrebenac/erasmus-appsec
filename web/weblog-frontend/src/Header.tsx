import * as React from 'react';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { useNavigate } from 'react-router-dom';

interface HeaderProps {
  title: string;
}

export default function Header(props: HeaderProps) {
  const { title } = props;

  let navigate = useNavigate();

  return (
    <React.Fragment>
      <Toolbar sx={{ borderBottom: 1, borderColor: 'divider', marginBottom: 2 }}>
        <Typography
          component="h2"
          variant="h4"
          color="inherit"
          align="left"
          noWrap
          sx={{ flex: 1 }}
        >
          {title}
        </Typography>
        <Button variant="outlined" size="small" sx={{ marginRight: 2 }} onClick={() => { navigate("/login") }}>
          Sign in
        </Button>
        <Button variant="outlined" size="small" onClick={() => { navigate("/register") }}>
          Sign up
        </Button>
      </Toolbar>
    </React.Fragment>
  );
}