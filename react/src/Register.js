import React, { useRef, useState } from "react";
import styled from "styled-components";
import axios from "axios";
import { API_URL } from "./config";
import { Link } from "react-router-dom";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

const Container = styled.div`
  max-width: 400px;
  width: 100%;
`;

function Register() {
  const usernameRef = useRef(null);
  const emailRef = useRef(null);
  const passwordRef = useRef(null);

  const [completed, setCompleted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (document.forms[0].reportValidity()) {
      axios
        .post(
          API_URL + "/api/account_register/",
          {
            username: usernameRef.current.value,
            email: emailRef.current.value,
            password: passwordRef.current.value,
          },
          {
            withCredentials: true,
          }
        )
        .then((response) => {
          if (response.data.result) {
            setCompleted(true);
          } else {
            window.alert(response.data.message);
          }
        })
        .catch((error) => {
          console.log("エラーが発生しました" + error);
          alert("通信に失敗しました");
        });
    }
  };
  return (
    <Container className="border rounded mx-auto bg-white">
      {!completed ? (
        <form onSubmit={handleSubmit}>
          <div className="border-bottom p-3">
            <h4 className="m-0">新規登録</h4>
          </div>
          <div className="border-bottom p-3">
            <label>ユーザ名:</label>
            <input
              ref={usernameRef}
              maxLength="20"
              required
              className="w-100"
            ></input>
          </div>
          <div className="border-bottom p-3">
            <label>メールアドレス:</label>
            <input
              ref={emailRef}
              type="email"
              required
              className="w-100"
            ></input>
          </div>
          <div className="border-bottom p-3">
            <label>パスワード:</label>
            <input
              ref={passwordRef}
              type="password"
              minLength="8"
              maxLength="20"
              required
              className="w-100"
            ></input>
          </div>
          <div className="border-bottom p-3">
            <button className="btn btn-primary">送信</button>
          </div>
        </form>
      ) : (
        <div className="border-bottom p-3">
          メールを送信しました。<br></br>
          24時間以内にURLから登録を完了してください。<br></br>
          <br></br>
          ＊メールアドレスによってはメールが受信されない場合がございます。
          <br></br>
          <br></br>
          <Link to="/">TOPへ戻る</Link>
        </div>
      )}
    </Container>
  );
}

export default Register;
