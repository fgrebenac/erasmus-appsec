import React from 'react';
import './App.css';
import Blog from './pages/Blog';
import {
  BrowserRouter,
  Routes,
  Route,
} from "react-router-dom";
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import BlogPost from './pages/BlogPost';
import NewBlogPost from './pages/NewBlogPost';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Blog />} />
        <Route path="login" element={<SignIn />} />
        <Route path="register" element={<SignUp />} />
        <Route path="user/:userId/post/:postId" element={<BlogPost />} />
        <Route path="newpost" element={<NewBlogPost />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
