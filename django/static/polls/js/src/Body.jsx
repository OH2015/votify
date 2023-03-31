import React, { useState, useEffect } from "react";
import styled, { keyframes } from "styled-components";
import Post from "./Post";
import QuestionForm from "./QuestionForm";

const RootElement = styled.div`
  max-width: 800px;
  margin: auto;
  text-align: center;
`;

export const RoundButton = styled.button`
  width: 35px;
  height: 35px;
  border-radius: 50%;
  background-color: #2196f3;
  border: none;
  position: relative;
  overflow: hidden;
  cursor: pointer;
`;

export const PlusIcon = styled.span`
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

const Loading = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.2);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
`;

const spin = keyframes`
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
`;

const Spiner = styled.div`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: 5px solid #fff;
  border-top-color: #3498db;
  animation: ${spin} 0.8s ease-in-out infinite;
`;

// ボディコンポーネント
const Body = () => {
  const [posts, setPosts] = useState([]); //投稿一覧
  const [showPopup, setShowPopup] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [userId, setUserId] = useState(0);
  const [votedList, setVotedList] = useState([]); // 投票済みのリスト

  const handleOpenPopup = () => {
    if (userId === 0) {
      alert("投稿するにはログインが必要です");
      return;
    }
    setShowPopup(true);
  };

  const handleClosePopup = () => {
    setShowPopup(false);
  };

  const get_voted = (question_id) => {
    return votedList.find((voted) => voted["question"] === question_id) || null;
  };

  // 初期処理
  useEffect(() => {
    // URLパラメータを取得
    const questionId = new URLSearchParams(window.location.search).get(
      "question_id"
    );
    const getQuestions = async () => {
      const url = "/api/question/";
      // パラメータが存在したらAPIのパラメータに追加
      if (questionId) url += `?question_id=${questionId}`;
      // 投稿一覧取得
      const res = await axios.get(url);
      // ログイン中のユーザのID取得
      const res2 = await axios.get("/api/get_user_id/");
      // 投票済みのリスト取得
      const result = await axios.get(`/api/get_voted_list`);
      setPosts(res.data);
      setUserId(res2.data.user_id);
      setVotedList(result.data);
    };
    getQuestions();
  }, []);

  return (
    <RootElement>
      {isLoading && (
        <Loading>
          <Spiner></Spiner>
        </Loading>
      )}

      <RoundButton onClick={handleOpenPopup}>
        <PlusIcon></PlusIcon>
      </RoundButton>
      {showPopup && <QuestionForm userId={userId} handleClosePopup={handleClosePopup} />}
      {posts.map((post) => (
        <Post
          key={post.id}
          {...post}
          setIsLoading={setIsLoading}
          userId={userId}
          voted={get_voted(post.id)}
        />
      ))}
    </RootElement>
  );
};

export default Body;
