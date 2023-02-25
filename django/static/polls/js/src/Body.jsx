import React, { useState, useEffect } from "react";
import styled from "styled-components";
import Post from "./Post";
import QuestionForm from "./QuestionForm";

const RootElement = styled.div`
  max-width: 800px;
  margin: auto;
  text-align: center;
`;

const RoundButton = styled.button`
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background-color: #2196f3;
  border: none;
  position: relative;
  overflow: hidden;
  cursor: pointer;
  margin-bottom: 25px;
`;

const PlusIcon = styled.span`
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  margin: auto;
  width: 10px;
  height: 10px;
  &::before,
  &::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    bottom: 0;
    right: 0;
    margin: auto;
    width: 2px;
    height: 10px;
    background-color: white;
  }
  &::before {
    transform: rotate(90deg);
  }
  &::after {
    transform: rotate(180deg);
  }
`;



// ボディコンポーネント
const Body = () => {
  const [posts, setPosts] = useState([]); //投稿一覧
  const [showPopup, setShowPopup] = useState(false);

  const handleOpenPopup = () => {
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  // 初期処理
  useEffect(() => {
    const getQuestions = async () => {
      const res = await axios.get("/api/questions/");
      setPosts(res.data);
    };
    getQuestions();
  }, []);

  return (
    <RootElement>
      <RoundButton onClick={handleOpenPopup}>
        <PlusIcon></PlusIcon>
      </RoundButton>
      {showPopup && <QuestionForm handleClosePopup={handleClosePopup}/>}
      {posts.map((post) => (
        <Post key={post.id} {...post} />
      ))}
    </RootElement>
  );
};

export default Body;
