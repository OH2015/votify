import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import axios from "axios";
import { API_URL } from "./config";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const Container = styled.div`
  max-width: 600px;
`;

const QuestionContainer = styled.div`
  background-color: #f5f5f5;
  margin-bottom: 20px;
  width: 100%;
  border: gray 1px solid;
  border-radius: 5px;
  padding: 5px;
  box-shadow: 3px 3px 3px;
`;

const QuestionHeader = styled.div`
  display: flex;
  justify-content: space-between;
`;

function AccountTop() {
  const [user, setUser] = useState({
    username: "ロード中...",
    email: "ロード中...",
    profile: "ロード中...",
    auth_provider: "",
  });
  const [questions, setQuestions] = useState([]);

  const getUserInfo = () => {
    axios
      .get(`${API_URL}/api/get_user_info/`, { withCredentials: true })
      .then((response) => {
        if (!response.data.result) {
          window.location.href = "/login";
        } else {
          setUser({
            ...user,
            ...response.data.user,
          });
        }
      });
  };

  const getQuestions = () => {
    axios
      .get(`${API_URL}/api/question/?user_id=${user.id}`, {
        withCredentials: true,
      })
      .then((response) => {
        setQuestions(response.data);
      })
      .catch(() => {
        alert("API通信中にエラーが発生しました。");
      });
  };

  useEffect(() => {
    getUserInfo();
    getQuestions();
  }, []);

  return (
    <>
      <Container className="mx-auto">
        <div className="border rounded mb-2">
          <div
            className="border-bottom p-3 m-0 row bg-secondary"
            style={{ height: "200px" }}
          >
            <div>
              <i id="user-icon" className="fa-solid fa-circle-user fa-5x"></i>
            </div>
          </div>
          <div className="m-0 row">
            <h3 className="m-0">{user.username}</h3>
            <p className="m-0">{user.email}</p>
          </div>
          <div className="m-0 row" style={{ minHeight: "50px" }}>
            <p className="m-0">{user.profile}</p>
          </div>
        </div>
        {questions.map((question) => (
          <Link
            className="text-dark"
            to={`/?question_id=${question.id}`}
            style={{ textDecoration: "none" }}
          >
            <QuestionContainer>
              <QuestionHeader>
                <h3 style={{ textAlign: "right" }}>{question.title}</h3>
                <span>{question.votes}票</span>
              </QuestionHeader>
            </QuestionContainer>
          </Link>
        ))}
      </Container>
    </>
  );
}

export default AccountTop;
