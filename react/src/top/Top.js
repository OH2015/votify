import React, { useState, useEffect } from "react";
import styled, { keyframes } from "styled-components";
import Post from "./Post";
import axios from "axios";
import { API_URL } from "../config";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

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
const Top = () => {
  const [posts, setPosts] = useState([]); //投稿一覧
  const [user, setUser] = useState(0);
  const [isLoading, setIsLoading] = useState(false);

  const getQuestions = () => {
    // URLパラメータを取得
    const questionId = new URLSearchParams(window.location.search).get(
      "question_id"
    );
    let url = `${API_URL}/api/question/`;
    // パラメータが存在したらAPIのパラメータに追加
    if (questionId) url += `?question_id=${questionId}`;
    axios
      .get(url, { withCredentials: true })
      .then((response) => {
        setPosts(response.data);
      })
      .catch(() => {
        alert("API通信中にエラーが発生しました。");
      });
  };

  const getUserInfo = () => {
    axios
      .get(`${API_URL}/api/get_user_info/`, { withCredentials: true })
      .then((response) => {
        if (response.data.result) {
          setUser(response.data.user);
        }
      })
      .catch(() => {
        alert("API通信中にエラーが発生しました。");
      });
  };

  // 初期処理
  useEffect(() => {
    getQuestions();
    getUserInfo();
  }, []);

  return (
    <RootElement>
      {isLoading && (
        <Loading>
          <Spiner></Spiner>
        </Loading>
      )}

      {posts.map((post) => (
        <Post
          key={post.id}
          question={post}
          setIsLoading={setIsLoading}
          userId={user.id}
        />
      ))}
    </RootElement>
  );
};

export default Top;
