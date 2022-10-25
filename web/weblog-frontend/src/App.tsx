import React from 'react';
import './App.css';
import Blog from './Blog';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import SignIn from './SignIn';
import SignUp from './SignUp';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Blog />} />
        <Route path="login" element={<SignIn />} />
        <Route path="register" element={<SignUp />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
